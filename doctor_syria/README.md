# Doctor Syria Platform

Doctor Syria is a comprehensive healthcare platform that connects patients, doctors, pharmacies, laboratories, and pharmaceutical companies in Syria.

## Features

- User Management (Patients, Doctors, Pharmacies, Laboratories, Companies)
- Appointment Scheduling
- Electronic Medical Records
- Prescription Management
- Pharmacy Inventory Management
- Laboratory Test Management
- Real-time Chat (Coming Soon)

## Technology Stack

- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Cache: Redis
- Task Queue: Celery
- Real-time: Django Channels
- Authentication: JWT
- Payment: Stripe

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/doctor-syria.git
cd doctor-syria
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root and add your environment variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=doctor_syria
DB_USER=postgres
DB_PASSWORD=your-password
...
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

API documentation is available at `/api/docs/` when the server is running.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
