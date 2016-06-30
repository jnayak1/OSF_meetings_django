from django.contrib.auth.models import User, Group
from api.models import Submission, Conference
from rest_framework import serializers as ser
from django_countries.fields import CountryField

class UserSerializer(ser.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

class GroupSerializer(ser.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class AuthenticationSerializer(ser.Serializer):
    username = ser.CharField(required=True)
    password = ser.CharField(required=True)

    def validate(self, data):
        return data

class ConferenceSerializer(ser.ModelSerializer):
    title = ser.CharField(required=True)
    city = ser.CharField()
    state = ser.CharField()
    country = CountryField() #get country_dict working later
    eventStart = ser.DateTimeField(source='event_start', required=False)
    eventEnd = ser.DateTimeField(source='event_end', required=False)
    submissionStart = ser.DateTimeField(source='submission_start', required=False)
    submissionEnd = ser.DateTimeField(source='submission_end', required=False)
    logoUrl = ser.URLField(source='logo_url', allow_blank=True)
    description = ser.CharField(allow_blank=True)
    siteUrl = ser.URLField(source='site_url')

    # Later on add tags and sponsors back
    class Meta:
        model = Conference
        fields = ('created', 'modified', 'id', 'title', 'siteUrl', 'city', 'state', 'country', 'eventStart', 'eventEnd', 'submissionStart', 'submissionEnd', 'logoUrl', 'description')

class SubmissionSerializer(ser.HyperlinkedModelSerializer):
    conference = ser.PrimaryKeyRelatedField(queryset=Conference.objects.all())
    contributors = UserSerializer(many=True)
    node_id = ser.CharField(read_only=True)

    def create(self, validated_data):
        # look up contributors by ID
        contributors = validated_data['contributors']
        title = validated_data['title']
        description = validated_data['description']
        conference = validated_data['conference']
        submission = Submission.objects.create(title=title, description=description, conference=conference, approved=False)
        for contributor in contributors:
                submission.contributors.add(contributor)
        return submission


    class Meta:
        model = Submission
        fields = ('id', 'node_id', 'title', 'description', 'conference', 'contributors')
