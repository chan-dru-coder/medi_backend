from rest_framework import serializers
from accounts.models import DoctorProfile
from .models import DoctorAvailability

class DoctorListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    class Meta:
        model = DoctorProfile
        fields = [
            "id", "name", "email", "specialization", "qualification",
            "experience_years", "hospital", "bio", "rating", "review_count",
            "profile_image", "consultation_fee"
        ]

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ["id", "date", "start_time", "end_time", "is_available"]

class AppointmentSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    doctor_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    appointment_date = serializers.DateField()
    appointment_time = serializers.TimeField()
    status = serializers.CharField()

    def get_doctor_name(self, obj):
        return obj.doctor.user.full_name if hasattr(obj.doctor, "user") else None
    def get_patient_name(self, obj):
        return obj.patient.full_name if hasattr(obj.patient, "full_name") else None
