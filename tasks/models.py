from datetime import timedelta, datetime

from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
from deliverables.models import Deliverable
from projects.models import Project
from teams.models import TeamMember
from organizations.models import Organization

from projects.utils import daterange


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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    baseline_fte_days = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    team_member = models.ForeignKey(TeamMember, null=True, blank=True, on_delete=models.SET_NULL)
    resources_required = models.ManyToManyField(Resource, blank=True)

    parent_tasks = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='parent_tasks_set')

    complexity_drivers = models.ManyToManyField(ComplexityDriver, through='ComplexityRelationship')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True)

    percent_complete = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    is_the_reference_task = models.BooleanField(default=False)
    copied_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='copied_from_set')

    def __str__(self):
        return self.name

    @property
    def augmented_name(self):
        try:
            return ''.join([self.name, ' (', self.deliverable.workstream.name, ' - ', self.deliverable.name, ')'])
        except AttributeError:
            return self.name

    @property
    def augmented_name2(self):
        try:
            return ''.join([self.name, ' (', self.deliverable.project.name, ' - ',
                            self.deliverable.workstream.name, ' - ', self.deliverable.name, ')'])
        except AttributeError:
            return self.name

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

    def set_task_days_forward(self, parent_end):

        if not parent_end:
            parent_end = datetime.today()

        task_end = parent_end + timedelta(float(self.baseline_fte_days))

        self.taskday_set.all().delete()
        task_days = []
        for date in daterange(parent_end, task_end):
            task_days.append(TaskDay(date=date, allocation=1, task=self))

        TaskDay.objects.bulk_create(task_days)

    def set_task_days_backward(self, child_start):

        task_start = child_start - timedelta(float(self.baseline_fte_days))

        self.taskday_set.all().delete()
        task_days = []
        for date in daterange(task_start, child_start):
            task_days.append(TaskDay(date=date, allocation=1, task=self))

        TaskDay.objects.bulk_create(task_days)

    @property
    def start(self):
        """ get earliest start time from related TaskDays
        :return: earliest
        """
        earliest = list(self.taskday_set.aggregate(models.Min('date')).values())[0]
        return earliest

    @property
    def end(self):
        """ get latest end time from related TaskDays

        :return: latest
        """
        latest = list(self.taskday_set.aggregate(models.Max('date')).values())[0]
        return latest

    @property
    def earliest_possible_start(self):
        """ latest end time of all parent tasks

        :return: latest
        """

        # if the task has parent tasks, find the latest ending date.
        if self.parent_tasks.all().exists():
            task_ends = [task.end for task in self.parent_tasks.all()]
            earliest_start = max(task_ends)

        else:  # use the project start date as the earliest possible date
            earliest_start = self.project.start

        return earliest_start

    @property
    def leading_gap(self):
        """ get time between start time and latest end time of all parent tasks

        :return:
        """

        return self.start - self.earliest_possible_start

    @property
    def children(self):
        """ get all Tasks for which this task is a parent

        :return:
        """
        return self.parent_tasks_set.all()


class TaskDay(models.Model):
    date = models.DateField(null=True, blank=True)
    allocation = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ]
    )
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([str(self.task), str(self.date)])

    def shift_date(self, delta):
        self.date += delta
        self.save()

    def stretch(self, n_days):
        # set allocation for this taskday to 1/n_days
        self.allocation = 1 / n_days

        # increase date for all subsequent task_days in task by n-1
        for td in self.task.taskday_set.all():
            if td.date > self.date:
                td.shift_date(n_days - 1)

        # add n-1 task_days following this one
        task_days = []
        for date in daterange(self.date, self.date + timedelta(n_days - 1)):
            task_days.append(TaskDay(date=date, allocation=1 / n_days, task=self.task))

        TaskDay.objects.bulk_create(task_days)

        self.save()


class ComplexityRelationship(models.Model):
    name = models.CharField(max_length=50)
    complexity_driver = models.ForeignKey(ComplexityDriver, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_factor = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.name
