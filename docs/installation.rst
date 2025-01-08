التثبيت والإعداد
==============

متطلبات النظام
------------

* Python 3.13 أو أحدث
* PostgreSQL 13 أو أحدث
* Redis 6 أو أحدث
* وحدة معالجة تدعم CUDA (اختياري، للذكاء الاصطناعي)

التثبيت
------

1. استنساخ المشروع
~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/khaled8809/doctor-syria-v2.git
   cd doctor-syria-v2

2. إعداد البيئة الافتراضية
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # على Linux/Mac
   # أو
   venv\Scripts\activate  # على Windows

3. تثبيت المتطلبات
~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

4. إعداد قاعدة البيانات
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py migrate

5. إنشاء المستخدم المدير
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py createsuperuser

6. تشغيل الخادم
~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py runserver

الإعداد للإنتاج
-------------

1. إعداد المتغيرات البيئية
~~~~~~~~~~~~~~~~~~~~~~~~

قم بإنشاء ملف `.env` في المجلد الرئيسي وأضف المتغيرات التالية:

.. code-block:: bash

   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DATABASE_URL=postgres://user:password@host:port/dbname
   REDIS_URL=redis://host:port/0

2. إعداد Celery
~~~~~~~~~~~~~

.. code-block:: bash

   celery -A doctor_syria worker -l info
   celery -A doctor_syria beat -l info

3. إعداد Nginx
~~~~~~~~~~~

.. code-block:: nginx

   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static/ {
           alias /path/to/static/;
       }
       
       location /media/ {
           alias /path/to/media/;
       }
   }

4. إعداد SSL
~~~~~~~~~~

نوصي باستخدام Let's Encrypt للحصول على شهادة SSL مجانية:

.. code-block:: bash

   sudo certbot --nginx -d your-domain.com
