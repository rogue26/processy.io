from django.db import models
from users.models import CustomUser
from projects.models import Project


class TeamMember(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    project_availability = models.DecimalField(decimal_places=2, default=0, max_digits=3)


    def __str__(self):
        return ''.join([self.first_name, ' ', self.last_name])