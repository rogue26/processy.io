from collections import Counter

from django.db import models
from users.models import CustomUser
from projects.models import Project


class TeamMember(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
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

    def __str__(self):
        if self.user is not None:
            return self.user
        else:
            return ' '.join([self.first_name, self.last_name])
