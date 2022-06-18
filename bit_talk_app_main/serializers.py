from rest_framework import serializers
from .models import Coins
# from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                 'id', 'username', 'first_name', 'last_name',
                 'email', 'last_login', 'gender', 'preffered_lang',
                 'dob', 'country', 'profile_image', 'preference',
                 'profile_updated', 'push_notifications',
                 'email_notifications', 'posts_visible',
                 'profile_photo_visible', 'last_seen_online'
                 )


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=True, required=True, validators=[EmailValidator])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'])
        user.first_name = validated_data['first_name']
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'first_name')

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        # instance.first_name = validated_data['first_name']
        instance.save()

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        token['displayname'] = user.first_name
        return token


class CoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins
        fields = '__all__'
