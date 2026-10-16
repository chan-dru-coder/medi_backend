from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.full_name", read_only=True)

    class Meta:
        model = Prescription
        fields = [
            "id", "appointment", "patient", "patient_name", "doctor",
            "doctor_name", "medical_notes", "prescription", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "patient", "doctor", "created_at", "updated_at"]

class PrescriptionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["id", "appointment", "medical_notes", "prescription", "created_at"]
