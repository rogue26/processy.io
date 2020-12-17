from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Partner'),
        (2, 'Director'),
        (3, 'Manager'),
        (4, 'Consultant')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)


class Client(models.Model):
    name = models.CharField(max_length=50)

    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    CLUSTER_CHOICES = [
        ('B2B', 'B2B'),
        ('SIM', 'SIM'),
        ('CPG', 'CPG'),
        ('BAN', 'Banking'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cluster = models.CharField(max_length=50, choices=CLUSTER_CHOICES)
    client = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_the_reference_project = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_the_reference_project:
            return super(Project, self).save(*args, **kwargs)
        with transaction.atomic():
            Project.objects.filter(
                is_the_reference_project=True).update(is_the_reference_project=False)
            return super(Project, self).save(*args, **kwargs)


class ScopeOfWork(models.Model):
    file = models.FileField(upload_to='SOWs')
