from .models import CustomUser, PatientProfile, DoctorProfile, Review, DoctorAvailability, TimeSlot
from .serializers import PatientProfileSerializer, DoctorProfileSerializer, ReviewSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from hospital.models import Department
from datetime import datetime
from rest_framework import generics
from .serializers import TimeSlotSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here.
        token['name'] = user.name
        token['is_patient'] = user.is_patient
        return token


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_complete=True)
        return Response(serializer.data)


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_complete=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_doctors_by_department(self, request):
        department_id = request.query_params.get('department_id')
        try:
            department = Department.objects.get(id=department_id)
            doctors = DoctorProfile.objects.filter(department=department)
            serializer = self.serializer_class(
                doctors, many=True, context={'request': request})
            return Response(serializer.data)
        except Department.DoesNotExist:
            return Response({'detail': f'Department with id {department_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class DoctorAvailabilityView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        try:
            date = datetime.strptime(self.kwargs['date'], "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = DoctorProfile.objects.get(id=self.kwargs['doctor_id'])
        except DoctorProfile.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            availability = DoctorAvailability.objects.get(
                doctor=doctor, date=date)
        except DoctorAvailability.DoesNotExist:
            return Response({'error': 'No availability for this doctor on this date'}, status=status.HTTP_404_NOT_FOUND)

        available_time_slots = []
        for time_slot in availability.time_slots.all():
            if DoctorAvailability.objects.is_time_slot_available(doctor, date, time_slot):
                available_time_slots.append(time_slot)

        return available_time_slots


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            payload = RefreshToken(token).payload
            user_id = payload['user_id']
            user = CustomUser.objects.get(id=user_id)
            print(user.id)
            if not user.is_active:
                user.is_active = True
                user.save()
                print(user.is_active)
                return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Account already activated'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
