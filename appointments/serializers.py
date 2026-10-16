from django.utils import timezone
from rest_framework import serializers
from accounts.models import DoctorProfile
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.user.full_name", read_only=True)
    specialization = serializers.CharField(source="doctor.specialization", read_only=True)
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "patient", "patient_name", "doctor", "doctor_name",
            "specialization", "appointment_date", "appointment_time",
            "status", "reason", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "patient", "status", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context["request"]
        if request.user.role != "patient":
            raise serializers.ValidationError({"detail": "Only patients can book appointments."})
        if attrs["appointment_date"] < timezone.localdate():
            raise serializers.ValidationError({"appointment_date": "Appointment date cannot be in the past."})
        return attrs

    def create(self, validated_data):
        validated_data["patient"] = self.context["request"].user
        return Appointment.objects.create(**validated_data)
