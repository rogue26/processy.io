from django.db import models, transaction
from workstreams.models import Workstream
from projects.models import Project


class DeliverableType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Deliverable(models.Model):
    FORMAT_CHOICES = [
        ('XLS', 'Excel tool'),
        ('PPT', 'PowerPoint deck'),
        ('PBI', 'Power BI dashboard'),
        ('TBL', 'Tableau dashboard'),
    ]

    description = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(DeliverableType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    scope = models.CharField(max_length=50, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    workstream = models.ForeignKey(Workstream, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    is_the_reference_deliverable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name


class Specification(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(SpecificationType, on_delete=models.CASCADE, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class ConditionType(models.Model):
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ConditionType, on_delete=models.CASCADE, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
