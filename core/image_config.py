"""
Image configuration settings
"""

# إعدادات الصور
IMAGE_SETTINGS = {
    'THUMBNAIL_SIZE': (300, 300),
    'PROFILE_PICTURE_SIZE': (150, 150),
    'LARGE_IMAGE_SIZE': (1200, 800),
    'ALLOWED_EXTENSIONS': ['jpg', 'jpeg', 'png', 'gif'],
    'MAX_UPLOAD_SIZE': 5242880,  # 5MB
    'COMPRESSION_QUALITY': 80,
}

# إعدادات التحميل الكسول
LAZY_LOADING_SETTINGS = {
    'ENABLED': True,
    'PLACEHOLDER': 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"%3E%3C/svg%3E',
    'THRESHOLD': 0.1,
}

from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, Adjust, SmartResize

class ThumbnailSpec(ImageSpec):
    processors = [SmartResize(width=300, height=300)]
    format = 'JPEG'
    options = {'quality': 80}

class ProfilePictureSpec(ImageSpec):
    processors = [
        SmartResize(width=150, height=150),
        Adjust(contrast=1.2, sharpness=1.1)
    ]
    format = 'JPEG'
    options = {'quality': 85}

class LargeImageSpec(ImageSpec):
    processors = [
        ResizeToFill(width=1200, height=800),
        Adjust(contrast=1.1)
    ]
    format = 'JPEG'
    options = {'quality': 75}

# تسجيل المواصفات
register.generator('thumbnail', ThumbnailSpec)
register.generator('profile_picture', ProfilePictureSpec)
register.generator('large_image', LargeImageSpec)
