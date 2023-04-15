from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, MyTokenObtainPairView, UserViewSet, PatientProfileViewSet, DoctorProfileViewSet, ReviewViewSet, ActivateAccountView, DoctorAvailabilityViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'patients', PatientProfileViewSet)
router.register(r'doctors', DoctorProfileViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'doctor_avail', DoctorAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name="sign_up"),
    path('auth/activate/<str:token>/', ActivateAccountView.as_view(),
         name='activate_account'),
]
