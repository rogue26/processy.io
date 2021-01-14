from django.db import models


class ScopeOfWork(models.Model):
    file = models.FileField(upload_to='SOWs')
