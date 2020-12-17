from django.db import models, transaction
from projects.models import Project


class WorkstreamType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Workstream(models.Model):
    """
    Abstract base class
    """

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    objective = models.CharField(max_length=50, blank=True)
    motivation = models.CharField(max_length=50, blank=True)
    owner = models.CharField(max_length=50, blank=True)
    # deliverables = models.ManyToManyField(Deliverable, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(WorkstreamType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    is_the_reference_workstream = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_the_reference_workstream:
            return super(Workstream, self).save(*args, **kwargs)
        with transaction.atomic():
            # make sure that no other workstreams of this type are tagged as reference workstream
            # to prevent any problems related to this, make sure that is_the_reference_workstream isn't shown in any
            # forms available to users.
            Workstream.objects.filter(
                is_the_reference_workstream=True, category=self.category).update(is_the_reference_workstream=False)
            return super(Workstream, self).save(*args, **kwargs)
