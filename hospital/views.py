from rest_framework import generics
from rest_framework import viewsets
from .models import Department, Appointment
from .serializers import DepartmentSerializer, AppointmentSerializer
from rest_framework import status
from users.models import DoctorProfile
from rest_framework.response import Response
from rest_framework.decorators import action


class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Appointment.objects.filter(user=user)
        return Appointment.objects.none()
