from collections import Counter

from django.db import models
from django.conf import settings

from projects.models import Project


class TeamMember(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    project_availability = models.DecimalField(decimal_places=2, default=0, max_digits=3)

    def calc_utilization_schedule(self):
        # create dictionary of dates and utilization

        # todo - eventually, this will need to sum up the allocation number for each taskday rather than simply count
        #  the taskdays

        # todo - I feel like there's a way to do this in one query, but I can't figure it out.
        teammember_tasks = self.task_set.all()
        teammember_task_days = [td.date for task in teammember_tasks for td in task.taskday_set.all()]
        return Counter(teammember_task_days)

    def stretch_overallocated_days(self):
        overallocated_days = {key: value for key, value in self.calc_utilization_schedule().items() if value > 1}

        for date, allocation in overallocated_days.items():
            # get taskdays for that day for this teammember
            tasks = self.task_set.all()
            overallocated_taskdays = [td for task in tasks for td in task.taskday_set.all() if td.date == date]

            # stretch those taskdays
            for td in overallocated_taskdays:
                td.stretch(allocation)


    def __str__(self):
        if self.user is not None:
            return self.user.email
        else:
            return ' '.join([self.first_name, self.last_name])
