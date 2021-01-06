from django.db import models, transaction
from projects.models import Project
from organizations.models import Organization


class WorkstreamType(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)

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
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(WorkstreamType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    is_the_reference_workstream = models.BooleanField(default=False)
    copied_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='copied_from_set')

    def __str__(self):
        return self.name

    @property
    def augmented_name(self):
        return ''.join([self.name, ' (', self.project.name, ')'])

    @property
    def augmented_name2(self):
        return ''.join([self.name, ' (', self.project.name, ')'])

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
