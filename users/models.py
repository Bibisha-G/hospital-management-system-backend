from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    age = models.IntegerField(default=18)
    avatar_slug = models.URLField(max_length=500)
    is_complete = models.BooleanField(default=False)
    info = models.CharField(max_length=220, null=True, blank=True)

    class Meta:
        abstract = True


class PatientProfile(Profile):
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name}"


class DoctorProfile(Profile):
    specialization = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=500)
    treatments = models.CharField(max_length=999)
    experience = models.PositiveIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=True, blank=True, related_name='doctors')

    def __str__(self):
        return f"{self.user.name}"


class DoctorAvailabilityManager(models.Manager):
    def is_time_slot_available(self, doctor, date, time_slot):
        availability = self.get(doctor=doctor, date=date)
        if time_slot in availability.time_slots.all():
            return not Appointment.objects.filter(doctor=doctor, date=date, time_slot=time_slot).exists()
        return False


class DoctorAvailability(models.Model):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
    ]

    doctor = models.ForeignKey(
        'DoctorProfile', on_delete=models.CASCADE, related_name='availability')
    day = models.IntegerField(choices=WEEKDAYS, validators=[
                              MaxValueValidator(5)])
    time_slots = models.ManyToManyField('TimeSlot')

    objects = DoctorAvailabilityManager()

    class Meta:
        unique_together = ('doctor', 'day',)


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    online_appointment_charge = models.PositiveIntegerField()
    physical_appointment_charge = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class Review(models.Model):
    doctor = models.ForeignKey(
        'DoctorProfile', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, max_length=999)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.doctor.user.name} by {self.reviewer.name}"

    def clean(self):
        # Check if the reviewer is the same as the doctor
        if self.doctor.user == self.reviewer:
            raise ValidationError('A doctor cannot give a review to himself.')


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    time_slot = models.ForeignKey(
        'users.TimeSlot', on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    appointment_charge = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"Appointment of {self.patient.user.name} with {self.doctor.user.name} on {formatted_date}"
