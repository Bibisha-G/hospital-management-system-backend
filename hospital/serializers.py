from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    doctors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'
