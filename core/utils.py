"""
Utility functions for optimizing image and file loading
"""

import os

from django.conf import settings
from django.core.cache import cache
from PIL import Image


def optimize_image(image_path, quality=85):
    """
    تحسين جودة الصورة وضغطها
    """
    try:
        img = Image.open(image_path)

        # حفظ النسبة الأصلية للصورة
        if img.size[0] > 1200 or img.size[1] > 1200:
            output_size = (1200, 1200)
            img.thumbnail(output_size)

        # تحويل الصور إلى JPEG للضغط الأفضل
        if img.format != "JPEG":
            img = img.convert("RGB")

        # حفظ الصورة المضغوطة
        img.save(image_path, "JPEG", quality=quality, optimize=True)
        return True
    except Exception as e:
        print(f"Error optimizing image: {str(e)}")
        return False


def get_cached_image_url(image_field, size="medium"):
    """
    الحصول على رابط الصورة المخزنة مؤقتاً
    """
    if not image_field:
        return None

    cache_key = f"image_url_{image_field.name}_{size}"
    cached_url = cache.get(cache_key)

    if cached_url:
        return cached_url

    # إنشاء نسخة مصغرة إذا لم تكن موجودة
    try:
        img_url = create_thumbnail(image_field, size)
        cache.set(cache_key, img_url, timeout=settings.CACHE_TTL)
        return img_url
    except Exception as e:
        print(f"Error creating thumbnail: {str(e)}")
        return image_field.url


def create_thumbnail(image_field, size="medium"):
    """
    إنشاء نسخة مصغرة من الصورة
    """
    sizes = {"small": (100, 100), "medium": (300, 300), "large": (600, 600)}

    if size not in sizes:
        size = "medium"

    try:
        img = Image.open(image_field.path)
        output_size = sizes[size]
        img.thumbnail(output_size)

        # إنشاء مسار للنسخة المصغرة
        filename = os.path.basename(image_field.name)
        thumbnail_name = f"thumb_{size}_{filename}"
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, "thumbnails", thumbnail_name)

        # التأكد من وجود مجلد النسخ المصغرة
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

        # حفظ النسخة المصغرة
        img.save(thumbnail_path, quality=85, optimize=True)

        # إرجاع الرابط النسبي
        return os.path.join(settings.MEDIA_URL, "thumbnails", thumbnail_name)
    except Exception as e:
        print(f"Error in create_thumbnail: {str(e)}")
        return image_field.url
