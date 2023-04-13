
from rest_framework import serializers
from .models import CustomUser, PatientProfile, DoctorProfile, Review
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings


def get_access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "name",
                  "password", "is_active", "is_patient", "is_doctor"]

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        token = get_access_token(user)

        # Send activation email
        send_mail(
            'Activate your account',
            f'Click the following link to activate your account: {settings.CLIENT_URL}/auth/activate/{token}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        # Call the clean() method before creating the review
        review = Review(**validated_data)
        review.clean()
        review.save()
        return review


class DoctorProfileSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = DoctorProfile
        fields = '__all__'
