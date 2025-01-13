import logging
import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)


class ImageProcessor:
    """معالج الصور"""

    def __init__(self, max_size=(800, 800), quality=85, format="JPEG"):
        self.max_size = max_size
        self.quality = quality
        self.format = format

    def process_image(self, image_field):
        """معالجة الصورة"""
        if not image_field:
            return None

        try:
            # فتح الصورة
            image = Image.open(image_field)

            # تحويل الصورة إلى RGB إذا كانت RGBA
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # تدوير الصورة حسب بيانات EXIF
            image = ImageOps.exif_transpose(image)

            # تغيير حجم الصورة
            image.thumbnail(self.max_size, Image.LANCZOS)

            # حفظ الصورة
            output = BytesIO()
            image.save(output, format=self.format, quality=self.quality, optimize=True)
            output.seek(0)

            # إنشاء اسم الملف الجديد
            filename = os.path.splitext(os.path.basename(image_field.name))[0]
            new_filename = f"{filename}_processed.{self.format.lower()}"

            # حفظ الصورة المعالجة
            return ContentFile(output.getvalue(), new_filename)

        except Exception as e:
            logger.error(f"خطأ في معالجة الصورة: {str(e)}")
            return None

    def create_thumbnail(self, image_field, size=(100, 100)):
        """إنشاء صورة مصغرة"""
        if not image_field:
            return None

        try:
            # فتح الصورة
            image = Image.open(image_field)

            # تحويل الصورة إلى RGB إذا كانت RGBA
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # إنشاء الصورة المصغرة
            thumbnail = ImageOps.fit(image, size, Image.LANCZOS)

            # حفظ الصورة المصغرة
            output = BytesIO()
            thumbnail.save(output, format=self.format, quality=self.quality)
            output.seek(0)

            # إنشاء اسم الملف الجديد
            filename = os.path.splitext(os.path.basename(image_field.name))[0]
            new_filename = f"{filename}_thumb.{self.format.lower()}"

            return ContentFile(output.getvalue(), new_filename)

        except Exception as e:
            logger.error(f"خطأ في إنشاء الصورة المصغرة: {str(e)}")
            return None

    def optimize_storage(self, image_field):
        """تحسين تخزين الصور"""
        if not image_field:
            return None

        try:
            # معالجة الصورة
            processed_image = self.process_image(image_field)
            if not processed_image:
                return None

            # حذف الصورة القديمة
            old_path = image_field.name
            if default_storage.exists(old_path):
                default_storage.delete(old_path)

            return processed_image

        except Exception as e:
            logger.error(f"خطأ في تحسين تخزين الصورة: {str(e)}")
            return None

    @staticmethod
    def validate_image(image_field):
        """التحقق من صحة الصورة"""
        if not image_field:
            return False

        try:
            # فتح الصورة للتحقق
            image = Image.open(image_field)
            image.verify()
            return True
        except Exception:
            return False

    def process_medical_image(self, image_field):
        """معالجة الصور الطبية"""
        if not image_field:
            return None

        try:
            # فتح الصورة
            image = Image.open(image_field)

            # تحسين التباين
            image = ImageOps.autocontrast(image)

            # تحسين السطوع
            image = ImageOps.equalize(image)

            # حفظ الصورة
            output = BytesIO()
            image.save(
                output, format=self.format, quality=100
            )  # جودة عالية للصور الطبية
            output.seek(0)

            # إنشاء اسم الملف الجديد
            filename = os.path.splitext(os.path.basename(image_field.name))[0]
            new_filename = f"{filename}_medical.{self.format.lower()}"

            return ContentFile(output.getvalue(), new_filename)

        except Exception as e:
            logger.error(f"خطأ في معالجة الصورة الطبية: {str(e)}")
            return None
