from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, PatientProfile, DoctorProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role", "phone", "profile_image", "created_at"]
        read_only_fields = ["id", "created_at"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["full_name", "email", "password", "role", "phone"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user.role == User.Role.DOCTOR:
            DoctorProfile.objects.create(
                user=user, specialization="General Physician",
                qualification="MBBS", experience_years=0
            )
        else:
            PatientProfile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        attrs["user"] = user
        return attrs

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PatientProfile
        fields = "__all__"

class DoctorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = DoctorProfile
        fields = [
            "id", "user", "name", "email", "specialization", "qualification",
            "experience_years", "hospital", "bio", "rating", "review_count",
            "profile_image", "consultation_fee", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "user", "rating", "review_count", "created_at", "updated_at"]
