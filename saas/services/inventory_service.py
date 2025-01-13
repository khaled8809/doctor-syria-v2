from django.db import transaction
from django.db.models import F, Q, Sum
from django.utils import timezone

from ..models import (
    InventoryItem,
    InventoryTransaction,
    MedicalCompany,
    MedicalSupply,
    PurchaseOrder,
    PurchaseOrderItem,
    Warehouse,
)


class InventoryService:
    @staticmethod
    def get_low_stock_items(tenant):
        """Get items that are below their minimum quantity."""
        low_stock_items = []
        supplies = MedicalSupply.objects.filter(tenant=tenant, is_active=True)

        for supply in supplies:
            total_quantity = (
                InventoryItem.objects.filter(
                    supply=supply, tenant=tenant, is_quarantined=False
                ).aggregate(total=Sum("quantity"))["total"]
                or 0
            )

            if total_quantity < supply.minimum_quantity:
                low_stock_items.append(
                    {
                        "supply": supply,
                        "current_quantity": total_quantity,
                        "minimum_quantity": supply.minimum_quantity,
                        "shortage": supply.minimum_quantity - total_quantity,
                    }
                )

        return low_stock_items

    @staticmethod
    def get_expiring_items(tenant, days=90):
        """Get items that will expire within the specified number of days."""
        expiry_date = timezone.now().date() + timezone.timedelta(days=days)
        return InventoryItem.objects.filter(
            tenant=tenant,
            expiry_date__lte=expiry_date,
            expiry_date__gte=timezone.now().date(),
            quantity__gt=0,
        ).order_by("expiry_date")

    @staticmethod
    def get_expired_items(tenant):
        """Get expired items that still have quantity."""
        return InventoryItem.objects.filter(
            tenant=tenant, expiry_date__lt=timezone.now().date(), quantity__gt=0
        ).order_by("expiry_date")

    @staticmethod
    @transaction.atomic
    def receive_inventory(
        tenant,
        supply,
        warehouse,
        batch_number,
        quantity,
        unit_price,
        manufacturing_date,
        expiry_date,
        location_in_warehouse,
        performed_by,
        reference_number,
        notes="",
    ):
        """Receive new inventory into the warehouse."""
        # Create or update inventory item
        inventory_item, created = InventoryItem.objects.get_or_create(
            tenant=tenant,
            supply=supply,
            warehouse=warehouse,
            batch_number=batch_number,
            defaults={
                "quantity": 0,
                "unit_price": unit_price,
                "manufacturing_date": manufacturing_date,
                "expiry_date": expiry_date,
                "location_in_warehouse": location_in_warehouse,
            },
        )

        if not created:
            inventory_item.quantity += quantity
            inventory_item.save()
        else:
            inventory_item.quantity = quantity
            inventory_item.save()

        # Create transaction record
        InventoryTransaction.objects.create(
            tenant=tenant,
            inventory_item=inventory_item,
            transaction_type="RECEIVE",
            quantity=quantity,
            reference_number=reference_number,
            destination_location=warehouse,
            performed_by=performed_by,
            notes=notes,
        )

        return inventory_item

    @staticmethod
    @transaction.atomic
    def dispense_inventory(
        tenant, inventory_item, quantity, performed_by, reference_number, notes=""
    ):
        """Dispense inventory from the warehouse."""
        if inventory_item.quantity < quantity:
            raise ValueError("Insufficient quantity available")

        if inventory_item.is_quarantined:
            raise ValueError("Cannot dispense quarantined items")

        if inventory_item.is_expired:
            raise ValueError("Cannot dispense expired items")

        # Update inventory quantity
        inventory_item.quantity -= quantity
        inventory_item.save()

        # Create transaction record
        transaction = InventoryTransaction.objects.create(
            tenant=tenant,
            inventory_item=inventory_item,
            transaction_type="DISPENSE",
            quantity=quantity,
            reference_number=reference_number,
            source_location=inventory_item.warehouse,
            performed_by=performed_by,
            notes=notes,
        )

        return transaction

    @staticmethod
    @transaction.atomic
    def transfer_inventory(
        tenant,
        inventory_item,
        destination_warehouse,
        quantity,
        performed_by,
        reference_number,
        new_location_in_warehouse,
        notes="",
    ):
        """Transfer inventory between warehouses."""
        if inventory_item.quantity < quantity:
            raise ValueError("Insufficient quantity available")

        # Create new inventory item in destination warehouse
        new_item = InventoryItem.objects.create(
            tenant=tenant,
            supply=inventory_item.supply,
            warehouse=destination_warehouse,
            batch_number=inventory_item.batch_number,
            quantity=quantity,
            unit_price=inventory_item.unit_price,
            manufacturing_date=inventory_item.manufacturing_date,
            expiry_date=inventory_item.expiry_date,
            location_in_warehouse=new_location_in_warehouse,
            is_quarantined=inventory_item.is_quarantined,
            quarantine_reason=inventory_item.quarantine_reason,
        )

        # Update source inventory quantity
        inventory_item.quantity -= quantity
        inventory_item.save()

        # Create transaction record
        transaction = InventoryTransaction.objects.create(
            tenant=tenant,
            inventory_item=inventory_item,
            transaction_type="TRANSFER",
            quantity=quantity,
            reference_number=reference_number,
            source_location=inventory_item.warehouse,
            destination_location=destination_warehouse,
            performed_by=performed_by,
            notes=notes,
        )

        return new_item, transaction

    @staticmethod
    @transaction.atomic
    def adjust_inventory(
        tenant, inventory_item, new_quantity, performed_by, reference_number, notes=""
    ):
        """Adjust inventory quantity for reconciliation."""
        old_quantity = inventory_item.quantity
        quantity_difference = new_quantity - old_quantity

        # Update inventory quantity
        inventory_item.quantity = new_quantity
        inventory_item.save()

        # Create transaction record
        transaction = InventoryTransaction.objects.create(
            tenant=tenant,
            inventory_item=inventory_item,
            transaction_type="ADJUST",
            quantity=quantity_difference,
            reference_number=reference_number,
            source_location=inventory_item.warehouse,
            performed_by=performed_by,
            notes=notes,
        )

        return transaction

    @staticmethod
    @transaction.atomic
    def quarantine_inventory(
        tenant, inventory_item, reason, performed_by, reference_number, notes=""
    ):
        """Place inventory items in quarantine."""
        inventory_item.is_quarantined = True
        inventory_item.quarantine_reason = reason
        inventory_item.save()

        # Create transaction record
        transaction = InventoryTransaction.objects.create(
            tenant=tenant,
            inventory_item=inventory_item,
            transaction_type="ADJUST",
            quantity=0,
            reference_number=reference_number,
            source_location=inventory_item.warehouse,
            performed_by=performed_by,
            notes=f"Quarantined: {reason}\n{notes}",
        )

        return transaction

    @staticmethod
    def get_inventory_value(tenant, warehouse=None):
        """Calculate total value of inventory."""
        query = Q(tenant=tenant)
        if warehouse:
            query &= Q(warehouse=warehouse)

        return (
            InventoryItem.objects.filter(query).aggregate(
                total_value=Sum(F("quantity") * F("unit_price"))
            )["total_value"]
            or 0
        )

    @staticmethod
    def get_inventory_summary(tenant, warehouse=None):
        """Get summary of inventory status."""
        query = Q(tenant=tenant)
        if warehouse:
            query &= Q(warehouse=warehouse)

        total_items = InventoryItem.objects.filter(query).count()
        total_value = InventoryService.get_inventory_value(tenant, warehouse)
        expired_items = InventoryItem.objects.filter(
            query, expiry_date__lt=timezone.now().date(), quantity__gt=0
        ).count()
        quarantined_items = InventoryItem.objects.filter(
            query, is_quarantined=True
        ).count()

        return {
            "total_items": total_items,
            "total_value": total_value,
            "expired_items": expired_items,
            "quarantined_items": quarantined_items,
        }

    @staticmethod
    def get_inventory_movements(tenant, supply=None, warehouse=None, days=30):
        """Get inventory movement history."""
        query = Q(tenant=tenant)
        if supply:
            query &= Q(inventory_item__supply=supply)
        if warehouse:
            query &= Q(Q(source_location=warehouse) | Q(destination_location=warehouse))

        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return InventoryTransaction.objects.filter(
            query, created_at__gte=cutoff_date
        ).order_by("-created_at")

    @staticmethod
    def get_supply_transactions(tenant, supply, days=30):
        """Get transaction history for a specific supply."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return InventoryTransaction.objects.filter(
            tenant=tenant, inventory_item__supply=supply, created_at__gte=cutoff_date
        ).order_by("-created_at")
