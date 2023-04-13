from django.db import models
from users.models import CustomUser


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
