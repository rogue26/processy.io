from django.db import transaction
from django.db import models

from users.models import CustomUser
from organizations.models import Division, Organization


class Client(models.Model):
    name = models.CharField(max_length=50)

    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    INTERNAL_EXTERNAL_CHOICES = [("internal", 'Internal'), ("external", 'External')]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    client = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_the_reference_project = models.BooleanField(default=False)
    internal = models.CharField(max_length=10, choices=INTERNAL_EXTERNAL_CHOICES, default="external", null=True)

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
