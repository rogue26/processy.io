from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True)

    # todo: incorporate address plugin
    address = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
