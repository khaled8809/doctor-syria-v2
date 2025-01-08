واجهة برمجة التطبيقات (API)
==========================

نظرة عامة
--------

يوفر نظام Doctor Syria واجهة برمجة تطبيقات (API) كاملة تتيح التكامل مع الأنظمة الأخرى. يستخدم النظام Django REST framework ويدعم:

* مصادقة JWT
* تحكم بالصلاحيات
* تصفية وترتيب النتائج
* صفحات النتائج
* توثيق تلقائي

نقاط النهاية الرئيسية
------------------

المرضى
~~~~~

.. code-block:: text

   GET /api/patients/
   POST /api/patients/
   GET /api/patients/{id}/
   PUT /api/patients/{id}/
   DELETE /api/patients/{id}/

المواعيد
~~~~~~~

.. code-block:: text

   GET /api/appointments/
   POST /api/appointments/
   GET /api/appointments/{id}/
   PUT /api/appointments/{id}/
   DELETE /api/appointments/{id}/

الأطباء
~~~~~~

.. code-block:: text

   GET /api/doctors/
   POST /api/doctors/
   GET /api/doctors/{id}/
   PUT /api/doctors/{id}/
   DELETE /api/doctors/{id}/

العيادات
~~~~~~~

.. code-block:: text

   GET /api/clinics/
   POST /api/clinics/
   GET /api/clinics/{id}/
   PUT /api/clinics/{id}/
   DELETE /api/clinics/{id}/

المصادقة
-------

جميع نقاط النهاية تتطلب مصادقة باستخدام JWT. للحصول على الرمز:

.. code-block:: text

   POST /api/token/
   {
       "username": "your-username",
       "password": "your-password"
   }

استخدام الرمز في الطلبات:

.. code-block:: text

   Authorization: Bearer <your-token>

أمثلة
----

Python
~~~~~~

.. code-block:: python

   import requests

   # الحصول على الرمز
   response = requests.post(
       'https://your-domain.com/api/token/',
       json={'username': 'user', 'password': 'pass'}
   )
   token = response.json()['access']

   # استخدام API
   headers = {'Authorization': f'Bearer {token}'}
   response = requests.get(
       'https://your-domain.com/api/patients/',
       headers=headers
   )
   patients = response.json()

JavaScript
~~~~~~~~~

.. code-block:: javascript

   // الحصول على الرمز
   const response = await fetch('https://your-domain.com/api/token/', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
       },
       body: JSON.stringify({
           username: 'user',
           password: 'pass',
       }),
   });
   const { access } = await response.json();

   // استخدام API
   const patients = await fetch('https://your-domain.com/api/patients/', {
       headers: {
           'Authorization': `Bearer ${access}`,
       },
   }).then(res => res.json());
