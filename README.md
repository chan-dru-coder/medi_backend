# MediConnect Backend

Django REST Framework + MySQL backend for the MediConnect healthcare appointment platform.

## Stack

- Python 3
- Django
- Django REST Framework
- JWT (SimpleJWT)
- MySQL
- django-cors-headers
- Pillow
- python-dotenv
- drf-spectacular

## Setup

### 1. Create MySQL database

```sql
CREATE DATABASE mediconnect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Copy `.env.example` to `.env` and set your MySQL credentials.

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=mediconnect
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### 5. Migrate

```bash
python manage.py migrate
```

### 6. Create admin

```bash
python manage.py createsuperuser
```

### 7. Seed development data

```bash
python manage.py seed_data
```

Demo-only accounts created by the seed command:

- Patient: `rahul.patient@example.com` / `DemoPatient123!`
- Doctors: `arun.doctor@example.com`, `priya.doctor@example.com`, `rohan.doctor@example.com`, `sneha.doctor@example.com`
- Doctor password: `DemoDoctor123!`

Do not use these credentials in production.

### 8. Run

```bash
python manage.py runserver
```

API: http://127.0.0.1:8000/api/

Swagger: http://127.0.0.1:8000/api/docs/

Schema: http://127.0.0.1:8000/api/schema/

Admin: http://127.0.0.1:8000/admin/

## Main endpoints

### Authentication

- POST `/api/auth/register/`
- POST `/api/auth/login/`
- POST `/api/auth/token/refresh/`
- GET `/api/auth/me/`

### Doctors

- GET `/api/doctors/`
- GET `/api/doctors/<id>/`
- GET `/api/doctors/<id>/availability/`

Doctor list supports `search`, `specialization`, and DRF pagination.

### Appointments

- POST `/api/appointments/`
- GET `/api/appointments/my/`
- GET `/api/appointments/<id>/`
- PATCH `/api/appointments/<id>/cancel/`
- PATCH `/api/appointments/<id>/accept/`
- PATCH `/api/appointments/<id>/reject/`
- PATCH `/api/appointments/<id>/complete/`

### Prescriptions

- POST `/api/prescriptions/`
- GET `/api/prescriptions/<id>/`
- PATCH `/api/prescriptions/<id>/`
- GET `/api/prescriptions/appointment/<appointment_id>/`

### Dashboards

- GET `/api/patient/dashboard/`
- GET `/api/doctor/dashboard/`

## Frontend

The React frontend should use:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Send JWT access tokens as:

```http
Authorization: Bearer <access_token>
```

## Double-booking protection

Appointment creation is wrapped in a database transaction and locks the matching `DoctorAvailability` row with `select_for_update()` before checking active appointments. This is intentional because MySQL does not support Django's conditional unique constraints in the same way as PostgreSQL. Booking therefore requires a real available doctor slot and protects that slot from concurrent bookings.

## Testing

```bash
python manage.py test
```

## Production notes

Before production deployment:

- Generate a strong random `SECRET_KEY`.
- Set `DEBUG=False`.
- Restrict `ALLOWED_HOSTS`.
- Restrict CORS origins to the real frontend domain.
- Use HTTPS.
- Use secure database credentials.
- Configure a production media storage strategy.
- Review JWT lifetimes and refresh-token rotation.
- Do not use the demo credentials.
