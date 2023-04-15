from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    time_slot = models.ForeignKey(
        'users.TimeSlot', on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    appointment_charge = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment of {self.patient.name} with {self.doctor.name} at {self.start_time.strftime('%Y-%m-%d %H:%M')}"
