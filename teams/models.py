from django.db import models
from users.models import CustomUser
from projects.models import Project


class TeamMember(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    project_availability = models.DecimalField(decimal_places=2, default=0, max_digits=3)


    def __str__(self):
        try:
            return ''.join([self.first_name, ' ', self.last_name])
        except:
            return super(TeamMember).__str__()