from django.contrib import admin

# Register your models here.
from .models import CustomUser, DoctorProfile, PatientProfile

admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
