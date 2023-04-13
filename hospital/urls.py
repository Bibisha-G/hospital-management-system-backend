from django.urls import path, include
from .views import DepartmentList, DepartmentDetail, AppointmentViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('departments/', DepartmentList.as_view(), name='department_list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(),
         name='department_detail'),
]
