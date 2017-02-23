from __future__ import unicode_literals

from django.db import models

class users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(blank=True, null=True)

class travels(models.Model):
    user = models.ForeignKey('users')
    destination =  models.CharField(max_length = 45)
    description =  models.CharField(max_length = 1000)
    startdate = models.DateField()
    enddate = models.DateField()

class addeduser(models.Model):
    adduser = models.ForeignKey('users')
    addtravel = models.ForeignKey('travels')
