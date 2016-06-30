from django.contrib.auth.models import User, Group
from api.models import Submission, Conference
from api.serializers import UserSerializer, GroupSerializer
from rest_framework import generics, viewsets
from api.serializers import SubmissionSerializer, ConferenceSerializer, AuthenticationSerializer

from rest_framework_json_api.parsers import JSONParser as JSONAPIParser
import requests
from requests_oauth2 import OAuth2
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import authenticate, login
from rest_framework import status

USER_STORAGE = {}

class OsfAuthorizationUrl(APIView):
    def get(self, request, format=None):
        client_id  = 'd5c46638ed1d42b9977264d084875c5a'
        client_secret = 'Pxsc1AeBDHBNK5dNCrqjvYkonBKMXXSvNSoDyK84'
        oauth2_handler = OAuth2(client_id, client_secret, "https://staging-accounts.osf.io/", "http://localhost:8000/login", authorization_url='oauth2/authorize')
        authorization_url = oauth2_handler.authorize_url('osf.full_read osf.full_write', response_type='code')
        return Response(authorization_url)

class OsfAuthorizationCode(APIView):
    def get(self, request, format=None):
        uid = request.user.id
        CLIENT_ID  = 'd5c46638ed1d42b9977264d084875c5a'
        CLIENT_SECRET = 'Pxsc1AeBDHBNK5dNCrqjvYkonBKMXXSvNSoDyK84'
        REDIRECT_URI = "http://localhost:8000/login"
        code = request.GET.get('code')
        post_data = { "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        response = requests.post("https://staging-accounts.osf.io/oauth2/token", data=post_data)
        USER_STORAGE[uid] = response
        return Response(USER_STORAGE[uid])

## List of conferences
class ConferenceList(generics.ListCreateAPIView):
    resource_name = 'conferences'
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer

## Detail of a conference
class ConferenceDetail(APIView):
    def get_object(self, pk):
        try:
            return Conference.objects.get(pk=pk)
        except Conference.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conference = self.get_object(pk)
        serializer = ConferenceSerializer(conference)
        return Response(serializer.data)

## List of submissions
class SubmissionList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    resource_name = 'Submission'
    encoding = 'utf-8'
    queryset= Submission.objects.all()

    def get(self, request, conference_id=None, format=None):
        conferenceSubmissions = Submission.objects.filter(conference_id=conference_id)
        submissionsSerializer = SubmissionSerializer(conferenceSubmissions, context={'request': request}, many=True)
        return Response(submissionsSerializer.data)

    def post(self, request, conference_id=None, format=None):
        serializer = SubmissionSerializer(data=request.data)
        contributors = [request.user.id]

        if serializer.is_valid():
            serializer.save(contributors=contributors)
            return Response(serializer.data)

        return Response(serializer.errors)

## Detail of a submission
class SubmissionDetail(APIView):
    resource_name = 'Submission'
    serializer_class = SubmissionSerializer

    def get(self, request, conference_id=None, submission_id=None , format=None):
        conferenceSubmission = Submission.objects.get(pk=submission_id)
        submissionsSerializer = SubmissionSerializer(conferenceSubmission, context={'request': request}, many=False)
        return Response(submissionsSerializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserDetail(APIView):
    resource_name = 'User'
    serializer_class = UserSerializer

    def get(self, request, user_id=None, format=None):
        user = User.objects.get(pk=user_id)
        userSerializer = UserSerializer(user, context={'request': request}, many=False)
        return Response(userSerializer.data)




class AuthenticateUser(APIView):
    resource_name = 'User'
    serializer_class = AuthenticationSerializer

    def post(self, request, format=None):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # the password verified for the user
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # the authentication system was unable to verify the username and password
                return Response("The username and password were not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Incorrect format for POST", status=status.HTTP_404_NOT_FOUND)
