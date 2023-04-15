from rest_framework import serializers
from .models import Department, Appointment

class DepartmentSerializer(serializers.ModelSerializer):
    doctors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')

    class Meta:
        model = Appointment
        fields = '__all__'
