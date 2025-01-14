from decimal import Decimal
from typing import List, Optional

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from ..models import (
    Cart,
    CartItem,
    InventoryItem,
    MedicalSupply,
    Order,
    OrderItem,
    Product,
    Review,
)


class ECommerceService:
    @staticmethod
    def list_products(
        category: Optional[str] = None,
        search_query: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        requires_prescription: Optional[bool] = None,
        available_only: bool = True,
    ) -> List[Product]:
        """
        List products with optional filtering.
        """
        products = Product.objects.all()

        if category:
            products = products.filter(category=category)

        if search_query:
            products = products.filter(name__icontains=search_query)

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        if requires_prescription is not None:
            products = products.filter(requires_prescription=requires_prescription)

        if available_only:
            products = products.filter(is_available=True)

        return products.select_related("medical_supply")

    @staticmethod
    def get_product_details(product_id: int) -> Product:
        """
        Get detailed information about a product.
        """
        return (
            Product.objects.select_related("medical_supply")
            .prefetch_related("reviews")
            .get(id=product_id)
        )

    @staticmethod
    def check_product_availability(product_id: int, quantity: int) -> bool:
        """
        Check if a product is available in the requested quantity.
        """
        product = Product.objects.get(id=product_id)
        if not product.is_available:
            return False

        total_inventory = (
            InventoryItem.objects.filter(
                supply=product.medical_supply, is_quarantined=False
            )
            .exclude(expiry_date__lt=timezone.now())
            .aggregate(total=models.Sum("quantity"))["total"]
            or 0
        )

        return total_inventory >= quantity

    @staticmethod
    @transaction.atomic
    def add_to_cart(
        user_id: int,
        product_id: int,
        quantity: int,
        prescription_file: Optional[str] = None,
    ) -> CartItem:
        """
        Add a product to the user's cart.
        """
        product = Product.objects.get(id=product_id)

        if not product.is_available:
            raise ValidationError("Product is not available")

        if quantity < product.min_order_quantity:
            raise ValidationError(
                f"Minimum order quantity is {product.min_order_quantity}"
            )

        if product.max_order_quantity and quantity > product.max_order_quantity:
            raise ValidationError(
                f"Maximum order quantity is {product.max_order_quantity}"
            )

        if product.requires_prescription and not prescription_file:
            raise ValidationError("Prescription is required for this product")

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "prescription": prescription_file},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    @staticmethod
    def get_cart(user_id: int) -> Cart:
        """
        Get the user's cart with all items.
        """
        return Cart.objects.prefetch_related("items__product").get_or_create(
            user_id=user_id
        )[0]

    @staticmethod
    @transaction.atomic
    def update_cart_item(cart_item_id: int, quantity: int) -> CartItem:
        """
        Update the quantity of a cart item.
        """
        cart_item = CartItem.objects.select_related("product").get(id=cart_item_id)

        if quantity < cart_item.product.min_order_quantity:
            raise ValidationError(
                f"Minimum order quantity is {cart_item.product.min_order_quantity}"
            )

        if (
            cart_item.product.max_order_quantity
            and quantity > cart_item.product.max_order_quantity
        ):
            raise ValidationError(
                f"Maximum order quantity is {cart_item.product.max_order_quantity}"
            )

        cart_item.quantity = quantity
        cart_item.save()

        return cart_item

    @staticmethod
    def remove_from_cart(cart_item_id: int):
        """
        Remove an item from the cart.
        """
        CartItem.objects.filter(id=cart_item_id).delete()

    @staticmethod
    @transaction.atomic
    def create_order(
        user_id: int, shipping_address: str, contact_phone: str, notes: str = ""
    ) -> Order:
        """
        Create an order from the user's cart.
        """
        cart = Cart.objects.prefetch_related("items__product").get(user_id=user_id)

        if not cart.items.exists():
            raise ValidationError("Cart is empty")

        # Calculate shipping fee based on order total
        total_amount = cart.total_amount
        shipping_fee = (
            Decimal("10.00") if total_amount < Decimal("100.00") else Decimal("0.00")
        )

        # Create order
        order = Order.objects.create(
            user_id=user_id,
            shipping_address=shipping_address,
            contact_phone=contact_phone,
            total_amount=total_amount,
            shipping_fee=shipping_fee,
            notes=notes,
        )

        # Create order items
        order_items = []
        for cart_item in cart.items.all():
            if not ECommerceService.check_product_availability(
                cart_item.product.id, cart_item.quantity
            ):
                raise ValidationError(
                    f"Product {cart_item.product.name} is not available in requested quantity"
                )

            order_items.append(
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.price,
                    prescription=cart_item.prescription,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        # Clear cart
        cart.items.all().delete()

        return order

    @staticmethod
    def get_order(order_id: int) -> Order:
        """
        Get order details.
        """
        return Order.objects.prefetch_related("items__product").get(id=order_id)

    @staticmethod
    def list_user_orders(user_id: int) -> List[Order]:
        """
        List all orders for a user.
        """
        return (
            Order.objects.filter(user_id=user_id)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    @staticmethod
    @transaction.atomic
    def update_order_status(order_id: int, status: str) -> Order:
        """
        Update the status of an order.
        """
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()

        # If order is cancelled, return items to inventory
        if status == "CANCELLED":
            for item in order.items.all():
                # Add inventory transaction to return items
                pass

        return order

    @staticmethod
    def create_review(
        user_id: int, product_id: int, rating: int, comment: str
    ) -> Review:
        """
        Create a product review.
        """
        if not Order.objects.filter(
            user_id=user_id, items__product_id=product_id, status="DELIVERED"
        ).exists():
            raise ValidationError("You can only review products you have purchased")

        return Review.objects.create(
            user_id=user_id, product_id=product_id, rating=rating, comment=comment
        )

    @staticmethod
    def get_product_reviews(product_id: int) -> List[Review]:
        """
        Get all reviews for a product.
        """
        return (
            Review.objects.filter(product_id=product_id)
            .select_related("user")
            .order_by("-created_at")
        )
