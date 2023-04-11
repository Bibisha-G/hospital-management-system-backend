from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PatientProfile, DoctorProfile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_patient:
            PatientProfile.objects.create(user=instance)
        elif instance.is_doctor:
            DoctorProfile.objects.create(user=instance)
