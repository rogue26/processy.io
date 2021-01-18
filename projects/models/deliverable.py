from django.db import models, transaction
from django.conf import settings

from projects.models import Workstream
from .project import Project

from organizations.models import Organization


class DeliverableType(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Deliverable(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(DeliverableType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    workstream = models.ForeignKey(Workstream, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    is_the_reference_deliverable = models.BooleanField(default=False)
    copied_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='copied_from_set')

    def __str__(self):
        return self.name

    @property
    def augmented_name(self):
        return ''.join([self.name, ' (', self.workstream.name, ')'])

    @property
    def augmented_name2(self):
        return ''.join([self.name, ' (', self.project.name, ' - ', self.workstream.name, ')'])

    def save(self, *args, **kwargs):
        if not self.is_the_reference_deliverable:
            return super(Deliverable, self).save(*args, **kwargs)
        with transaction.atomic():
            # make sure that no other deliverables of this type are tagged as reference deliverable
            # to prevent any problems related to this, make sure that is_the_reference_deliverable isn't shown in any
            # forms available to users.
            Workstream.objects.filter(
                is_the_reference_deliverable=True, category=self.category).update(is_the_reference_deliverable=False)
            return super(Deliverable, self).save(*args, **kwargs)


class SpecificationType(models.Model):
    name = models.CharField(max_length=50)
    deliverable_type = models.ForeignKey(DeliverableType, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Specification(models.Model):
    details = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(SpecificationType, on_delete=models.CASCADE, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.details


class ConditionType(models.Model):
    name = models.CharField(max_length=50)
    deliverable_type = models.ForeignKey(DeliverableType, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Condition(models.Model):
    details = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(ConditionType, on_delete=models.CASCADE, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.details
