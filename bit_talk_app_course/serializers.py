# from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Courses


class CourseSerializer(DocumentSerializer):
    # id = serializers.CharField(read_only=False)

    class Meta:
        model = Courses
        fields = '__all__'
        depth = 2
