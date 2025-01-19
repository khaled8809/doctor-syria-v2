"""
نظام توليد البطاقات التعريفية
"""

import os
from datetime import datetime
from io import BytesIO

import qrcode
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

from utils.barcode_generator import BarcodeGenerator


class IDCardGenerationError(Exception):
    """خطأ في إنشاء البطاقة التعريفية"""

    pass


class IDCardGenerator:
    """مولد البطاقات التعريفية"""

    def __init__(self):
        self.card_size = (1000, 600)  # حجم البطاقة
        self.background_color = (255, 255, 255)  # لون الخلفية
        self.text_color = (0, 0, 0)  # لون النص

        # استخدام الخط الافتراضي
        self.title_font = ImageFont.load_default()
        self.text_font = ImageFont.load_default()

    def create_card(self, user):
        """
        إنشاء بطاقة تعريفية للمستخدم
        """
        try:
            # إنشاء صورة جديدة
            card = Image.new("RGB", self.card_size, self.background_color)
            draw = ImageDraw.Draw(card)

            # إضافة العنوان
            title = "Doctor Syria - بطاقة تعريفية"
            draw.text((50, 50), title, font=self.title_font, fill=self.text_color)

            # إضافة معلومات المستخدم
            user_info = [
                f"الاسم: {user.get_full_name()}",
                f"البريد الإلكتروني: {user.email}",
                f"نوع المستخدم: {user.get_user_type_display()}",
                f"تاريخ الإنشاء: {datetime.now().strftime('%Y-%m-%d')}",
            ]

            y_position = 150
            for info in user_info:
                draw.text(
                    (50, y_position), info, font=self.text_font, fill=self.text_color
                )
                y_position += 40

            # إضافة الباركود
            barcode_generator = BarcodeGenerator()
            barcode = barcode_generator.generate(str(user.id))
            barcode_image = Image.open(BytesIO(barcode))
            card.paste(barcode_image, (50, y_position))

            # إضافة QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"https://doctor-syria.com/users/{user.id}")
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            card.paste(qr_image, (self.card_size[0] - 200, y_position))

            # حفظ البطاقة
            output = BytesIO()
            card.save(output, format="PNG")
            output.seek(0)
            return output

        except Exception as e:
            raise IDCardGenerationError(f"خطأ في إنشاء البطاقة التعريفية: {str(e)}")

    @staticmethod
    def generate_batch(users):
        """
        توليد بطاقات تعريفية لمجموعة من المستخدمين
        :param users: قائمة المستخدمين
        :return: قائمة بالنتائج
        """
        generator = IDCardGenerator()
        results = {"success": 0, "failed": 0, "errors": []}

        for user in users:
            try:
                generator.create_card(user)
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({"user": user.username, "error": str(e)})

        return results
