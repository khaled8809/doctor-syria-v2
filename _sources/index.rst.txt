نظام Doctor Syria لإدارة المستشفيات والعيادات الطبية
==========================================

.. toctree::
   :maxdepth: 2
   :caption: المحتويات:

   introduction
   installation
   modules/index
   api/index

مقدمة
-----

Doctor Syria هو نظام متكامل لإدارة المستشفيات والعيادات الطبية في سوريا. يوفر النظام العديد من الميزات المتقدمة مثل:

* إدارة المرضى والمواعيد
* إدارة الأطباء والعيادات
* نظام الوصفات الطبية
* إدارة المخزون الطبي
* التقارير والإحصائيات
* نظام الفوترة والمحاسبة

التثبيت
-------

.. code-block:: bash

   git clone https://github.com/khaled8809/doctor-syria-v2.git
   cd doctor-syria-v2
   python -m venv venv
   source venv/bin/activate  # على Linux/Mac
   # أو
   venv\Scripts\activate  # على Windows
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
