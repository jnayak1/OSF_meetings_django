from __future__ import unicode_literals
from django.contrib.auth.models import User, Group

from django.db import models


# Create your models here.
class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    submissionDate = models.DateField()
    closeDate = models.DateField()
    logo = models.ImageField(upload_to='logo_folder/')
    tags = models.CharField(max_length=500)
    sponsors = models.CharField(max_length=500, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ('created',)


class Node(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    contributors = models.ForeignKey(Group)
    description = models.TextField()
    keywords = models.CharField(max_length=500)
    meeting = models.ManyToManyField(Meeting)

    class Meta:
        ordering = ('created',)


class SubmissionEval(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    premise = models.IntegerField()
    research = models.IntegerField()
    style = models.IntegerField()
    comment = models.TextField()
    total = models.IntegerField()

    class Meta:
        ordering = ('created',)


