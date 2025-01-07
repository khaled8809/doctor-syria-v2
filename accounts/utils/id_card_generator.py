"""
نظام توليد البطاقات التعريفية
"""
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
import os
from django.conf import settings
from datetime import datetime
from utils.barcode_generator import BarcodeGenerator

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
        # إنشاء صورة جديدة
        card = Image.new('RGB', self.card_size, self.background_color)
        draw = ImageDraw.Draw(card)
        
        # محاولة إضافة الشعار
        try:
            logo_path = os.path.join(settings.STATIC_ROOT, 'img', 'logo.png')
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo = logo.resize((150, 150))
                card.paste(logo, (50, 50))
        except Exception as e:
            print(f"تعذر إضافة الشعار: {str(e)}")
        
        # إضافة عنوان البطاقة
        draw.text((400, 50), "بطاقة تعريفية", font=self.title_font, fill=self.text_color)
        
        # إضافة معلومات المستخدم
        y_position = 200
        draw.text((50, y_position), f"الاسم: {user.get_full_name()}", font=self.text_font, fill=self.text_color)
        y_position += 50
        draw.text((50, y_position), f"الدور: {user.role}", font=self.text_font, fill=self.text_color)
        y_position += 50
        draw.text((50, y_position), f"تاريخ الإنشاء: {user.created_at.strftime('%Y-%m-%d')}", font=self.text_font, fill=self.text_color)
        
        # إضافة الباركود
        try:
            barcode_path = BarcodeGenerator.generate_user_id_barcode(user)
            if barcode_path:
                barcode_full_path = os.path.join(settings.MEDIA_ROOT, barcode_path)
                if os.path.exists(barcode_full_path):
                    barcode = Image.open(barcode_full_path)
                    barcode = barcode.resize((200, 200))
                    card.paste(barcode, (700, 300))
        except Exception as e:
            print(f"تعذر إضافة الباركود: {str(e)}")
        
        # حفظ البطاقة
        card_filename = f"id_card_{user.id}.png"
        card_path = os.path.join(settings.ID_CARDS_DIR, card_filename)
        card.save(card_path)
        
        return f"id_cards/{card_filename}"
    
    @staticmethod
    def generate_batch(users):
        """
        توليد بطاقات تعريفية لمجموعة من المستخدمين
        :param users: قائمة المستخدمين
        :return: قائمة بالنتائج
        """
        generator = IDCardGenerator()
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for user in users:
            try:
                generator.create_card(user)
                results['success'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'user': user.username,
                    'error': str(e)
                })
        
        return results
