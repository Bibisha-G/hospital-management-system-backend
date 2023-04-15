from rest_framework import generics
from rest_framework import viewsets
from .models import Department, Appointment
from .serializers import DepartmentSerializer, AppointmentSerializer
from rest_framework import status
from users.models import DoctorProfile,PatientProfile

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
        
    @action(detail=False, methods=['get'])
    def get_appointments_by_doctor(self, request):
        doctor_id = request.query_params.get('doctor_id')
        print(doctor_id)

        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)            
            apointments = Appointment.objects.filter(doctor=doctor.user.id)
            print(apointments)
            serializer = self.serializer_class(
                apointments, many=True, context={'request': request})
            return Response(serializer.data)
        except DoctorProfile.DoesNotExist:
            return Response({'detail': f'Doctor with id {doctor_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
