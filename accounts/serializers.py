from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    def validate_email(self, email):
        email = super().validate_email(email)
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return email


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'birthday', 'address', 'mobile', 'date_joined']
        read_only_fields = ['id', 'username', 'email']  # These fields cannot be updated