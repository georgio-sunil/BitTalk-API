from django.contrib.auth.models import AnonymousUser
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import MongoUser


class MongoUserSerializer(DocumentSerializer):
    class Meta:
        model = MongoUser
        fields = '__all__'
        depth = 1


class MongoUserResponseSerializer(DocumentSerializer):
    class Meta:
        model = MongoUser
        fields = ['username', 'first_name', 'last_name', 'password',
                  'gender', 'preffered_lang', 'dob', 'country',
                  'profile_image', 'preference', 'profile_updated',
                  'push_notifications', 'email_notifications',
                  'posts_visible', 'profile_photo_visible',
                  'last_seen_online', 'last_login', 'date_joined']
        depth = 1


class MongoUserLoginSerializer(DocumentSerializer):
    class Meta:
        model = MongoUser
        fields = ['username', 'password']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = 'username'
    user = AnonymousUser()

    @classmethod
    def get_token(cls, user):
        # user =  AnonymousUser()
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        # token['displayname'] = user.first_name
        return token
