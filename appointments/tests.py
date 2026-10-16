from datetime import date, time, timedelta
from rest_framework.test import APITestCase
from accounts.models import User, DoctorProfile

class AppointmentTests(APITestCase):
    def setUp(self):
        self.patient = User.objects.create_user(
            email="patient@example.com", password="StrongPassword123!",
            full_name="Patient One", role="patient"
        )
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com", password="StrongPassword123!",
            full_name="Doctor One", role="doctor"
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user, specialization="Cardiologist",
            qualification="MBBS, MD", experience_years=8
        )
        self.client.force_authenticate(self.patient)

    def test_patient_can_book(self):
        response = self.client.post("/api/appointments/", {
            "doctor": self.doctor.id,
            "appointment_date": str(date.today() + timedelta(days=2)),
            "appointment_time": "10:00:00",
            "reason": "Routine consultation"
        }, format="json")
        self.assertEqual(response.status_code, 201)
