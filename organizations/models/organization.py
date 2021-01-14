from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True, blank=True)

    letterhead = models.FileField(upload_to='Letterhead', null=True, blank=True)
    ppt_template = models.FileField(upload_to='PPT Templates', null=True, blank=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     # todo: throw error if domain is set to be the same as an existing domain
    #     return super(Organization, self).save(*args, **kwargs)


class Division(models.Model):
    name = models.CharField(max_length=50, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name