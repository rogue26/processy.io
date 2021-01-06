from datetime import datetime
from django.db import transaction, models

from users.models import CustomUser
from organizations.models import Division, Organization


class Client(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True)

    # todo: incorporate address plugin
    address = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
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

    @property
    def start(self):
        return min(task.start for task in self.task_set.all())

    @property
    def end(self):
        return max(task.end for task in self.task_set.all())

    @property
    def duration(self):
        tasks = self.task_set.all()

        if tasks:
            task_starts = [task.start for task in tasks]
            task_ends = [task.end for task in tasks]
            return max(task_ends) - min(task_starts)
        else:
            return 0

    @staticmethod
    def recursive_set_dates_forward(tasks, parent_end=None):
        for task in tasks:

            if parent_end is None:
                parent_end = datetime.today()

            # if task has no TaskDays, then set them up.
            if not task.taskday_set.all().exists:
                task.set_task_days_forward(parent_end)

            if task.children:
                # for each child, create a new set of task days working forward
                for child in task.children:
                    child.set_task_days_forward(parent_end)
                Project.recursive_set_dates_forward(tasks=task.children)
            else:
                # task has no children, se we just need to create the set of taskdays for it here
                task.set_task_days_forward(parent_end)

    @staticmethod
    def recursive_set_dates_backward(tasks, child_start=None):

        for task in tasks:

            if child_start is None:
                child_start = datetime.today()

            # if task does not have TaskDays, create them. This should only apply to the tasks without children from
            # which we are working backward.
            if not task.taskday_set.all().exists():
                task.set_task_days_backward(child_start)

            # for each parent, create a new set of task days working backward from current task
            if task.parent_tasks.all().exists():
                for parent in task.parent_tasks.all():
                    # if parent does not have TaskDays, create them, working backward from current task.start
                    if not parent.taskday_set.all().exists():
                        parent.set_task_days_backward(task.start)
                    else:  # parent already has TaskDays created. Check if parent ends after current task.start
                        if parent.end > task.start:
                            # parent is ending after child task has started. Parent task TaskDays need to be reset
                            parent.set_task_days_backward(child_start)
                        else:
                            # parent ends before child has started. do nothing.
                            pass
                Project.recursive_set_dates_backward(tasks=task.parent_tasks.all())

    def setup_gantt(self, optimize=False):

        # the first step is to delete all TaskDays for all tasks in the project. The alternative is to do a bunch of
        # senseless checking later to make sure that the TaskDays still make sense after whatever changes were
        # made to get the user to refresh the project dashboard page.

        all_tasks = self.task_set.all()
        for task in self.task_set.all():
            task.taskday_set.all().delete()

        # the recursive part start with the tasks with no children and recursively works its way through the parents,
        # adjusting their TaskDays earlier when necessary to prevent them from overlapping with tasks for which they
        # are prerequisites
        no_child_tasks = [task for task in all_tasks if not task.children]
        Project.recursive_set_dates_backward(no_child_tasks, child_start=datetime.today())

        # the recursion arbitrarily sets "today" as the end point for the childless tasks. (We don't know the actual
        # end date unless we do a "forward" construction of the gantt chart, but we'd end up just having to do
        # a backward construction anyway, so it's easier to just do the backward one and then shift everything
        # forward to start either at the project start date or today, whichever is later.
        duration = self.duration

        for task in all_tasks:
            for taskday in task.taskday_set.all():
                taskday.shift_date(duration)

        for i, task in enumerate(self.task_set.all()):
            print(i, task, task.start, task.end)

        # if optimize:
        #     for team_member in self.team_members:
        #         team_member.calc_utilization_schedule
        #         team_member.optimize_utilization_schedule


class ScopeOfWork(models.Model):
    file = models.FileField(upload_to='SOWs')
