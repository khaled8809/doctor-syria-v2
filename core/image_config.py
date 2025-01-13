"""
Image configuration settings
"""

# إعدادات تحسين الصور
IMAGE_SETTINGS = {
    'THUMBNAIL_SIZES': {
        'small': (100, 100),
        'medium': (300, 300),
        'large': (600, 600),
        'original': None
    },
    'COMPRESSION_QUALITY': 85,
    'MAX_UPLOAD_SIZE': 5 * 1024 * 1024,  # 5MB
    'ALLOWED_EXTENSIONS': ['jpg', 'jpeg', 'png', 'gif'],
    'AUTO_OPTIMIZE': True,
}

# إعدادات التحميل الكسول
LAZY_LOADING_SETTINGS = {
    'ENABLE': True,
    'THRESHOLD_SIZE': 100 * 1024,  # 100KB
    'DEFAULT_PLACEHOLDER': 'static/images/placeholder.jpg',
    'LOADING_ANIMATION': True,
}

# إعدادات التخزين المؤقت للصور
IMAGE_CACHE_SETTINGS = {
    'ENABLE': True,
    'CACHE_TIMEOUT': 60 * 60 * 24,  # 24 hours
    'CACHE_KEY_PREFIX': 'img_cache_',
    'USE_COMPRESSION': True,
}
