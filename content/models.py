from django.db import models

from users.models import CustomUser
from tasks.models import Task
from deliverables.models import Deliverable
from workstreams.models import Workstream
from organizations.models import Organization


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
    uploaded_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ContentTag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)

    tasks = models.ManyToManyField(Task, blank=True)
    deliverables = models.ManyToManyField(Deliverable, blank=True)
    workstreams = models.ManyToManyField(Workstream, blank=True)

    def __str__(self):
        return self.name
