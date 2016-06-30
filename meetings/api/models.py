from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.db import models

import datetime
from django_countries.fields import CountryField

# Create your models here.

class Submission(models.Model):
    node_id = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    contributors = models.ManyToManyField(User, blank=True)
    description = models.TextField()
    conference = models.ForeignKey('conference')
    approved = models.NullBooleanField(blank=True)

    class Meta:
        ordering = ('date_created',)

class Conference(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    site_url = models.URLField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = CountryField(blank_label='(select country)')
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)
    submission_start = models.DateTimeField(blank=True, null=True)
    submission_end = models.DateTimeField(blank=True, null=True)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True, max_length=500)

    class Meta:
        ordering = ('created',)
