web: gunicorn doctor_syria.wsgi:application
worker: celery -A doctor_syria worker -l info
beat: celery -A doctor_syria beat -l info
