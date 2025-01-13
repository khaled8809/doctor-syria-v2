import stripe
from django.conf import settings
from django.urls import reverse

from .models import Payment, StripePayment

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """خدمة للتعامل مع Stripe"""

    @staticmethod
    def create_payment_intent(payment):
        """إنشاء نية دفع في Stripe"""
        try:
            # تحويل المبلغ إلى أصغر وحدة عملة (بالسنت)
            amount_in_cents = int(payment.amount * 100)

            # إنشاء نية الدفع
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency="usd",  # يمكن تغييرها حسب العملة المطلوبة
                metadata={
                    "invoice_number": payment.invoice.invoice_number,
                    "payment_id": payment.id,
                },
            )

            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def confirm_payment(payment_intent_id):
        """تأكيد الدفع"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if intent.status == "succeeded":
                payment_id = intent.metadata.get("payment_id")
                payment = Payment.objects.get(id=payment_id)

                # إنشاء سجل StripePayment
                charge = intent.charges.data[0]
                StripePayment.objects.create(
                    payment=payment,
                    stripe_charge_id=charge.id,
                    stripe_payment_intent_id=payment_intent_id,
                    card_last4=charge.payment_method_details.card.last4,
                    card_brand=charge.payment_method_details.card.brand,
                )

                # تحديث حالة الدفع
                payment.status = "completed"
                payment.save()

                # تحديث حالة الفاتورة
                invoice = payment.invoice
                invoice.status = "paid"
                invoice.save()

                return True
            return False
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def create_refund(payment):
        """إنشاء استرداد في Stripe"""
        try:
            stripe_payment = payment.stripe_payment

            refund = stripe.Refund.create(charge=stripe_payment.stripe_charge_id)

            if refund.status == "succeeded":
                payment.status = "refunded"
                payment.save()

                invoice = payment.invoice
                invoice.status = "refunded"
                invoice.save()

                return True
            return False
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def get_payment_methods(customer_id):
        """الحصول على طرق الدفع المحفوظة للعميل"""
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id, type="card"
            )
            return payment_methods.data
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def create_customer(user, payment_method_id=None):
        """إنشاء عميل في Stripe"""
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.get_full_name(),
                payment_method=payment_method_id,
            )
            return customer
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def add_payment_method(customer_id, payment_method_id):
        """إضافة طريقة دفع جديدة للعميل"""
        try:
            payment_method = stripe.PaymentMethod.attach(
                payment_method_id, customer=customer_id
            )
            return payment_method
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def remove_payment_method(payment_method_id):
        """إزالة طريقة دفع"""
        try:
            stripe.PaymentMethod.detach(payment_method_id)
            return True
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def create_setup_intent(customer_id):
        """إنشاء نية إعداد لحفظ بطاقة جديدة"""
        try:
            setup_intent = stripe.SetupIntent.create(
                customer=customer_id, payment_method_types=["card"]
            )
            return setup_intent
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def handle_webhook(payload, sig_header):
        """معالجة Webhook من Stripe"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )

            if event.type == "payment_intent.succeeded":
                payment_intent = event.data.object
                StripeService.confirm_payment(payment_intent.id)

            elif event.type == "payment_intent.payment_failed":
                payment_intent = event.data.object
                payment_id = payment_intent.metadata.get("payment_id")
                payment = Payment.objects.get(id=payment_id)
                payment.status = "failed"
                payment.save()

            return True
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
        except Exception as e:
            raise Exception(f"Webhook error: {str(e)}")
