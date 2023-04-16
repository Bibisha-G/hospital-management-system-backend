from django.contrib import admin

# Register your models here.
from .models import CustomUser, DoctorProfile, PatientProfile, Review, DoctorAvailability, TimeSlot
from .models import Department, Appointment

admin.site.register(Department)
admin.site.register(Appointment)

admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(Review)
admin.site.register(DoctorAvailability)
admin.site.register(TimeSlot)
