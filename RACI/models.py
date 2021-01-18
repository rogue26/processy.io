from django.db import models
from organizations.models import Organization
from projects.models import Project


class RACI(models.Model):
    name = models.CharField(max_length=50, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    FREQUENCY_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    ]

    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=200, null=True)
    task_frequency = models.CharField(max_length=50, null=True, choices=FREQUENCY_CHOICES)

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=50, null=True)
    tools = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, null=True)
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE)


class Role(models.Model):
    name = models.CharField(max_length=50, null=True)
    task = models.ManyToManyField(Activity, blank=True, through='RACILevel')

    def __str__(self):
        return self.name


class RACILevel(models.Model):
    RACI_CHOICES = [
        ('R', 'Responsible'),
        ('A', 'Accountable'),
        ('C', 'Consulted'),
        ('I', 'Informed'),
    ]

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=RACI_CHOICES)
    raci = models.ForeignKey(RACI, on_delete=models.CASCADE)

    def __str__(self):
        return " - ".join([self.raci.name, self.role.name, self.activity.name, self.level])
