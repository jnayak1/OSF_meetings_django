from django.contrib.auth.models import User, Group
from api.models import Node, SubmissionEval, Meeting
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class NodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Node
		fields = ('id', 'title','meeting', 'contributors', 'description','keywords')


class SubmissionEvalSerializer(serializers.ModelSerializer):
	class Meta:
		model = SubmissionEval
		fields = ('id', 'created', 'premise', 'research','style', 'comment', 'total')

class MeetingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meeting
		fields = ('id', 'title', 'website', 'city', 
			'state', 'country', 'startDate', 'endDate', 
			'submissionDate', 'closeDate', 'logo', 'tags', 'sponsors', 'description')