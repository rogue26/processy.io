from django.db import models
from django.conf import settings
from django.apps import apps

from .organization import Organization

# from django.contrib.auth import get_user_model

# UserModel = get_user_model()
# CustomUser = apps.get_model('users', 'CustomUser')
# Task = apps.get_model('projects', 'Task')
# Deliverable = apps.get_model('projects', 'Deliverable')
# Workstream = apps.get_model('projects', 'Workstream')
# from users.models import CustomUser
# from django.contrib.auth.models import User
from projects.models import Task, Deliverable, Workstream

# from projects.models import Task, Deliverable, Workstream


class ContentType(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ContentDetail(models.Model):
    detail = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.detail


class ContentTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Content(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='knowledge management', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ContentTag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)

    tasks = models.ManyToManyField(Task, blank=True)
    deliverables = models.ManyToManyField(Deliverable, blank=True)
    workstreams = models.ManyToManyField(Workstream, blank=True)

    def __str__(self):
        return self.name
