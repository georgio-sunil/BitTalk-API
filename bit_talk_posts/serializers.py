# from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Posts


class PostsSerializer(DocumentSerializer):

    class Meta:
        model = Posts
        fields = '__all__'
        depth = 2
