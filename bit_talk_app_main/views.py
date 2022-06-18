import requests
from rest_framework import status
from rest_framework import generics
from .models import Coins
# from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    CoinsSerializer
    )
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from django.contrib.auth import login  # , logout
User = get_user_model()
from rest_framework_mongoengine.viewsets import ModelViewSet


class CoinsList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Coins.objects.all()
    serializer_class = CoinsSerializer


class CoinsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coins.objects.all()
    serializer_class = CoinsSerializer


class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    """
    Updating flag profile updated if few feilds are set,
    also converting preferences list to string before storing
    """
    def patch(self, request, *args, **kwargs):
        if (
                request.data.get('last_name') and
                request.data.get('dob') and
                request.data.get('gender') and
                request.data.get('country')
                ):
            request.data['profile_updated'] = True
        preferences = request.data.get('preference')
        if preferences is not None:
            preferences_str = ",".join(str(x) for x in preferences)
            request.data['preference'] = preferences_str
        return self.partial_update(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data['username']).count() == 1:
            return Response({"message": "User already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        post_response = self.create(request, *args, **kwargs)
        if post_response.status_code == 201:
            login_response = self.call_login_api(request)
            # post_response.data = {'msg': 'User registered successfully!'}
            return login_response
        return post_response

    def call_login_api(self, request):
        url = "http://127.0.0.1:8000/login/" # noqa
        body = {"username": request.data['username'], "password": request.data['password']} # noqa
        try:
            response = requests.post(url, json=body)
            return Response(response.json())
        except (ConnectionError) as e:
            print(e)


class ChangePasswordView(generics.UpdateAPIView):

    lookup_field = 'id'
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        update_response = self.update(request, *args, **kwargs)
        if update_response.status_code == 200:
            update_response.data = {'msg': 'Password changed successfully!'}
        return update_response


class CustomObtainTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        login(request, user)
        # Append user profile info to send along with refresh and access code.
        response.data['username'] = user.username
        response.data['first_name'] = user.first_name
        response.data['last_name'] = user.last_name
        response.data['email'] = user.email
        response.data['last_login'] = user.last_login
        response.data['gender'] = user.gender
        response.data['preffered_lang'] = user.preffered_lang
        response.data['dob'] = user.dob
        response.data['country'] = user.country
        response.data['profile_image'] = user.profile_image
        response.data['preference'] = user.preference
        response.data['profile_updated'] = user.profile_updated
        response.data['push_notifications'] = user.push_notifications
        response.data['email_notifications'] = user.email_notifications
        response.data['posts_visible'] = user.posts_visible
        response.data['profile_photo_visible'] = user.profile_photo_visible
        response.data['last_seen_online'] = user.last_seen_online
        return response


@api_view(['GET', 'POST'])
def password_reset_request(request):
    if request.method == "POST":
        associated_users = User.objects.filter(
                                    Q(username='nazia.fatima@wm-int.com'))
#  associated_users = User.objects.filter(username='nazia.fatima@wm-int.com')
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.txt"
                c = {
                    "email": user.username,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'fromadmin@example.com',
                              ['nazia.fatima@wm-int.com'], fail_silently=False)
                except BadHeaderError:
                    return Response({"message": "Invalid header found."})
                return Response({"message": "Email Sent."})
    else:
        send_mail('test_subject', 'test email body', 'fromadmin@example.com',
                  ['nazia.fatima@wm-int.com'], fail_silently=False)
        return Response({"message": "Test Email Sent."})


@api_view(['POST'])
def user_logout(request):

    if request.method == "POST":
        # logout(request)
        return Response({"message": "User logged out successfully."})

# class NewsFeedList(generics.ListCreateAPIView):
#     # permission_classes = (AllowAny,)
#     queryset = NewsFeed.objects.all()
#     serializer_class = NewsfeedSerializer


# class NewsFeedDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = NewsFeed.objects.all()
#     serializer_class = NewsfeedSerializer
