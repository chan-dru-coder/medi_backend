from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import DoctorProfile

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="availability")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["date", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "start_time"],
                name="unique_doctor_availability_start"
            )
        ]

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}"
