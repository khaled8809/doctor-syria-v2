import hashlib
import json
from datetime import datetime

import requests
from django.conf import settings


class FaturaService:
    """خدمة للتعامل مع بوابة الدفع Fatura"""

    BASE_URL = settings.FATURA_API_URL
    MERCHANT_ID = settings.FATURA_MERCHANT_ID
    API_KEY = settings.FATURA_API_KEY

    @classmethod
    def generate_signature(cls, data, timestamp):
        """إنشاء التوقيع للطلب"""
        string_to_hash = f"{cls.MERCHANT_ID}{timestamp}{cls.API_KEY}"
        for key in sorted(data.keys()):
            string_to_hash += str(data[key])

        return hashlib.sha256(string_to_hash.encode()).hexdigest()

    @classmethod
    def create_payment(cls, payment):
        """إنشاء طلب دفع جديد"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # تحضير بيانات الطلب
        data = {
            "merchantId": cls.MERCHANT_ID,
            "amount": int(payment.amount * 100),  # تحويل المبلغ إلى أصغر وحدة
            "currency": "SYP",
            "orderId": payment.invoice.invoice_number,
            "description": f"دفع الفاتورة {payment.invoice.invoice_number}",
            "returnUrl": settings.FATURA_RETURN_URL,
            "callbackUrl": settings.FATURA_CALLBACK_URL,
            "customerEmail": payment.invoice.patient.user.email,
            "customerName": payment.invoice.patient.user.get_full_name(),
            "customerPhone": payment.invoice.patient.phone,
            "timestamp": timestamp,
        }

        # إضافة التوقيع
        signature = cls.generate_signature(data, timestamp)
        headers = {
            "Content-Type": "application/json",
            "X-Signature": signature,
            "X-Timestamp": timestamp,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/payment/create", json=data, headers=headers
            )
            response.raise_for_status()

            result = response.json()
            if result["status"] == "success":
                return {
                    "payment_url": result["paymentUrl"],
                    "transaction_id": result["transactionId"],
                }
            else:
                raise Exception(result["message"])

        except requests.exceptions.RequestException as e:
            raise Exception(f"Fatura API error: {str(e)}")

    @classmethod
    def verify_payment(cls, transaction_id):
        """التحقق من حالة الدفع"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        data = {
            "merchantId": cls.MERCHANT_ID,
            "transactionId": transaction_id,
            "timestamp": timestamp,
        }

        signature = cls.generate_signature(data, timestamp)
        headers = {
            "Content-Type": "application/json",
            "X-Signature": signature,
            "X-Timestamp": timestamp,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/payment/verify", json=data, headers=headers
            )
            response.raise_for_status()

            result = response.json()
            return {
                "status": result["status"],
                "amount": result.get("amount", 0) / 100,  # تحويل المبلغ من أصغر وحدة
                "transaction_id": result["transactionId"],
                "payment_method": result.get("paymentMethod"),
                "payment_time": result.get("paymentTime"),
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Fatura API error: {str(e)}")

    @classmethod
    def refund_payment(cls, transaction_id, amount, reason):
        """استرداد المبلغ"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        data = {
            "merchantId": cls.MERCHANT_ID,
            "transactionId": transaction_id,
            "amount": int(amount * 100),  # تحويل المبلغ إلى أصغر وحدة
            "reason": reason,
            "timestamp": timestamp,
        }

        signature = cls.generate_signature(data, timestamp)
        headers = {
            "Content-Type": "application/json",
            "X-Signature": signature,
            "X-Timestamp": timestamp,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/payment/refund", json=data, headers=headers
            )
            response.raise_for_status()

            result = response.json()
            if result["status"] == "success":
                return {"refund_id": result["refundId"], "status": "success"}
            else:
                raise Exception(result["message"])

        except requests.exceptions.RequestException as e:
            raise Exception(f"Fatura API error: {str(e)}")

    @classmethod
    def verify_webhook_signature(cls, signature, timestamp, payload):
        """التحقق من صحة توقيع Webhook"""
        expected_signature = cls.generate_signature(payload, timestamp)
        return signature == expected_signature
