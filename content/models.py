from django.db import models

from users.models import CustomUser
from tasks.models import Task
from deliverables.models import Deliverable


class ContentType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ContentTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Content(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='Content', null=True, blank=True)
    uploaded_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, blank=True)
    tags = models.ManyToManyField(ContentTag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    deliverables = models.ManyToManyField(Deliverable, blank=True)
