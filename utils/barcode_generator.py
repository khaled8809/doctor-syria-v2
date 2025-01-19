"""
نظام توليد وقراءة الباركود
"""

import os
from io import BytesIO

import cv2
import numpy as np
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from django.conf import settings
from PIL import Image


class BarcodeGenerator:
    """مولد الباركود والQR"""

    @staticmethod
    def generate_barcode(data, barcode_type="code128", filename=None):
        """
        توليد باركود
        :param data: البيانات المراد تحويلها لباركود
        :param barcode_type: نوع الباركود (الافتراضي: code128)
        :param filename: اسم الملف المطلوب (اختياري)
        :return: مسار الصورة المولدة
        """
        try:
            # إنشاء مسار حفظ الباركود
            barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
            os.makedirs(barcode_dir, exist_ok=True)

            # تحديد اسم الملف
            if filename is None:
                filename = f"barcode_{data}"

            output_path = os.path.join(barcode_dir, f"{filename}.png")

            if barcode_type == "code128":
                # توليد باركود Code128
                code128 = Code128(str(data), writer=ImageWriter())
                code128.save(output_path)

            elif barcode_type == "qr":
                # توليد QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                qr_image = qr.make_image(fill_color="black", back_color="white")
                qr_image.save(output_path)

            else:
                raise ValueError(f"نوع الباركود غير مدعوم: {barcode_type}")

            return f"barcodes/{filename}.png"

        except Exception as e:
            raise Exception(f"خطأ في توليد الباركود: {str(e)}")

    @staticmethod
    def read_barcode(image_path):
        """
        قراءة الباركود من صورة
        :param image_path: مسار الصورة
        :return: البيانات المقروءة من الباركود
        """
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("لم يتم العثور على الصورة")

            # تحويل الصورة إلى تدرج رمادي
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # قراءة الباركود
            barcodes = cv2.barcode.BarcodeDetector()
            retval, decoded_info, decoded_type, points = barcodes.detectAndDecode(gray)

            if retval:
                return decoded_info[0]

            # محاولة قراءة QR code
            qr_decoder = cv2.QRCodeDetector()
            (
                retval,
                decoded_info,
                points,
                straight_qrcode,
            ) = qr_decoder.detectAndDecodeMulti(gray)

            if retval:
                return decoded_info[0]

            return None

        except Exception as e:
            raise Exception(f"خطأ في قراءة الباركود: {str(e)}")

    @staticmethod
    def generate_user_id_barcode(user):
        """
        توليد باركود لمعرف المستخدم
        :param user: كائن المستخدم
        :return: مسار الباركود المولد
        """
        try:
            # تجهيز البيانات
            data = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
            }

            # توليد اسم ملف آمن
            filename = f"user_{user.id}"

            # توليد باركود QR (يدعم بيانات أكثر)
            return BarcodeGenerator.generate_barcode(str(data), "qr", filename)

        except Exception as e:
            raise Exception(f"خطأ في توليد باركود المستخدم: {str(e)}")

    @staticmethod
    def generate_patient_id_card(patient):
        """
        توليد بطاقة مريض مع باركود
        :param patient: كائن المريض
        :return: مسار البطاقة المولدة
        """
        try:
            # إنشاء صورة البطاقة
            card = Image.new("RGB", (600, 400), "white")

            # إضافة بيانات المريض
            # TODO: إضافة النص والتصميم للبطاقة

            # إضافة الباركود
            barcode_path = BarcodeGenerator.generate_user_id_barcode(patient)
            barcode_image = Image.open(os.path.join(settings.MEDIA_ROOT, barcode_path))

            # دمج الباركود مع البطاقة
            card.paste(barcode_image, (400, 250))

            # حفظ البطاقة
            card_dir = os.path.join(settings.MEDIA_ROOT, "id_cards")
            os.makedirs(card_dir, exist_ok=True)
            card_path = os.path.join(card_dir, f"patient_card_{patient.id}.png")
            card.save(card_path)

            return f"id_cards/patient_card_{patient.id}.png"

        except Exception as e:
            raise Exception(f"خطأ في توليد بطاقة المريض: {str(e)}")
