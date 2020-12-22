from django.db import models, transaction
from deliverables.models import Deliverable
from projects.models import Project
from teams.models import TeamMember

class ComplexityDriver(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ResourceType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ResourceType, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    baseline_fte_hours = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    resources_required = models.ManyToManyField(Resource, blank=True)
    prerequisite_tasks = models.ManyToManyField('self', blank=True, symmetrical=False,
                                                related_name='prerequisite_tasks_set')
    complexity_drivers = models.ManyToManyField(ComplexityDriver, through='ComplexityRelationship')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    percent_complete = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    team_member = models.ForeignKey(TeamMember, null=True, blank=True, on_delete=models.CASCADE)

    is_the_reference_task = models.BooleanField(default=False)
    copied_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='copied_from_set')

    def __str__(self):
        return self.name

    @property
    def augmented_name(self):
        return ''.join([self.name, ' (', self.deliverable.workstream.name, ' - ', self.deliverable.name, ')'])

    @property
    def augmented_name2(self):
        return ''.join([self.name, ' (', self.deliverable.project.name,' - ',self.deliverable.workstream.name, ' - ', self.deliverable.name, ')'])


    def save(self, *args, **kwargs):
        if not self.is_the_reference_task:
            return super(Task, self).save(*args, **kwargs)
        with transaction.atomic():
            # make sure that no other tasks of this type are tagged as reference task
            # to prevent any problems related to this, make sure that is_the_reference_task isn't shown in any
            # forms available to users.
            Task.objects.filter(
                is_the_reference_task=True, category=self.category).update(is_the_reference_task=False)
            return super(Task, self).save(*args, **kwargs)


class ComplexityRelationship(models.Model):
    name = models.CharField(max_length=50)
    complexity_driver = models.ForeignKey(ComplexityDriver, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_factor = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.name
