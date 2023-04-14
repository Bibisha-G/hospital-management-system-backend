from django.urls import path, include
from .views import AppointmentViewSet, DepartmentViewset
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'departments', DepartmentViewset)

urlpatterns = [
    path('', include(router.urls)),
]
