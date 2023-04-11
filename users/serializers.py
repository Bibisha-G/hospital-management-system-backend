
from rest_framework import serializers
from .models import CustomUser, PatientProfile, DoctorProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "name",
                  "password", "is_patient", "is_doctor"]

    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'],
                                         name=validated_data['name'],
                                         is_patient=validated_data['is_patient'],
                                         is_doctor=validated_data['is_doctor'],

                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
