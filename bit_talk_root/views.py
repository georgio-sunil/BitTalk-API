from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import MongoUserSerializer, MongoUserResponseSerializer
from .models import MongoUser
from django.contrib.auth.hashers import check_password, make_password
from .utils import generate_access_token  # , generate_refresh_token


class MongoUserViewSet(ModelViewSet):
    serializer_class = MongoUserSerializer

    def validate_password(self, serializer):
        # password = serializer.validated_data['password']
        """
        Implement pwd validations later
        """
        return True

    def get_queryset(self):
        return MongoUser.objects.all()

    @action(detail=False, methods=['post'], url_path=r'register',)
    def register(self, request, *args, **kwargs):
        serializer = MongoUserResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.validate_password(serializer):
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password'])
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers)

    @action(detail=False, methods=['post'], url_path=r'login',)
    def login(self, request, *args, **kwargs):
        username = request.data['username']
        raw_password = request.data['password']
        try:
            user = MongoUser.objects.get(username=username)
        except Exception:
            return Response({"message": "Error identifying user"},
                            status=status.HTTP_401_UNAUTHORIZED)
        data = {}
        if check_password(raw_password, user.password):
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['last_login'] = user.last_login
            data['gender'] = user.gender
            data['preffered_lang'] = user.preffered_lang
            data['dob'] = user.dob
            data['country'] = user.country
            data['profile_image'] = user.profile_image
            data['preference'] = user.preference
            data['profile_updated'] = user.profile_updated
            data['push_notifications'] = user.push_notifications
            data['email_notifications'] = user.email_notifications
            data['posts_visible'] = user.posts_visible
            data['profile_photo_visible'] = user.profile_photo_visible
            data['last_seen_online'] = user.last_seen_online
            data['access'] = generate_access_token(user)
            # data['refresh']= generate_refresh_token(user)
            return Response(data, status=status.HTTP_200_OK)

        return Response(
                {"message": "Password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['patch'], url_path=r'change_password',)
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if self.validate_password(serializer):
            instance.password = make_password(
                serializer.validated_data['password'])
            instance.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                    headers=headers)
