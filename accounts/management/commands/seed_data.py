from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import DoctorProfile, PatientProfile, User
from doctors.models import DoctorAvailability
from appointments.models import Appointment

class Command(BaseCommand):
    help = "Create development/demo data for MediConnect."

    @transaction.atomic
    def handle(self, *args, **options):
        doctors = [
            ("Dr. Arun Kumar", "arun.doctor@example.com", "Cardiologist", "MBBS, MD", 8, "City Hospital, Bangalore", Decimal("1200.00"), Decimal("4.8"), 120),
            ("Dr. Priya Sharma", "priya.doctor@example.com", "Dermatologist", "MBBS, MD", 6, "MediCare Hospital", Decimal("1000.00"), Decimal("4.7"), 98),
            ("Dr. Rohan Mehta", "rohan.doctor@example.com", "Neurologist", "MBBS, MD", 10, "Apollo Medical Center", Decimal("1500.00"), Decimal("4.9"), 140),
            ("Dr. Sneha Patel", "sneha.doctor@example.com", "Pediatrician", "MBBS, MD", 7, "City Children's Hospital", Decimal("900.00"), Decimal("4.6"), 85),
        ]

        created_doctors = []
        for name, email, spec, qual, exp, hospital, fee, rating, reviews in doctors:
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={"full_name": name, "role": User.Role.DOCTOR}
            )
            if not user.has_usable_password():
                user.set_password("DemoDoctor123!")
                user.save()
            profile, _ = DoctorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "specialization": spec, "qualification": qual,
                    "experience_years": exp, "hospital": hospital,
                    "bio": f"Experienced {spec.lower()} focused on patient-centered care.",
                    "consultation_fee": fee, "rating": rating, "review_count": reviews
                }
            )
            created_doctors.append(profile)

        patient, _ = User.objects.get_or_create(
            email="rahul.patient@example.com",
            defaults={"full_name": "Rahul Sharma", "role": User.Role.PATIENT}
        )
        if not patient.has_usable_password():
            patient.set_password("DemoPatient123!")
            patient.save()
        PatientProfile.objects.get_or_create(user=patient)

        start = date.today() + timedelta(days=1)
        for doctor in created_doctors:
            for day_offset in range(5):
                d = start + timedelta(days=day_offset)
                for slot in [time(9,0), time(9,30), time(10,0), time(10,30), time(11,0), time(11,30)]:
                    DoctorAvailability.objects.get_or_create(
                        doctor=doctor, date=d, start_time=slot, end_time=(time(slot.hour, slot.minute + 30) if slot.minute == 0 else time(slot.hour + 1, 0))
                    )

        self.stdout.write(self.style.SUCCESS(
            "Seed complete. Demo patient: rahul.patient@example.com / DemoPatient123!; "
            "demo doctors use their email and password DemoDoctor123! (development only)."
        ))
