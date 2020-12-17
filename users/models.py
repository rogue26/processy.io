from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class Organization(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
