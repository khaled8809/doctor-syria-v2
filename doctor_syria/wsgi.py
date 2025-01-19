"""
WSGI config for doctor_syria project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctor_syria.settings_simple")

application = get_wsgi_application()
