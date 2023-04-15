from rest_framework import serializers
from .models import CustomUser, PatientProfile, DoctorProfile, Review, TimeSlot, DoctorAvailability

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from hospital.serializers import AppointmentSerializer


def get_access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)


class UserSerializer(serializers.ModelSerializer):
    profile_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "email", "name", "password", "is_active",
                  "is_patient", "is_doctor", "profile_id"]

    def get_profile_id(self, obj):
        try:
            if obj.is_patient:
                return obj.patientprofile.id
            elif obj.is_doctor:
                return obj.doctorprofile.id
        except:
            return None

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
    appointments_as_patient = AppointmentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

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
    appointments_as_doctor = AppointmentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('id', 'start_time', 'end_time',
                  'online_appointment_charge', 'physical_appointment_charge')


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True)

    class Meta:
        model = DoctorAvailability
        fields = ('id', 'doctor', 'day', 'time_slots')

    def create(self, validated_data):
        time_slots_data = validated_data.pop('time_slots')
        availability = DoctorAvailability.objects.create(**validated_data)
        for slot_data in time_slots_data:
            slot = TimeSlot.objects.get(pk=slot_data['id'])
            availability.time_slots.add(slot)
        return availability
