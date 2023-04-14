from .models import CustomUser, PatientProfile, DoctorProfile, Review
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
