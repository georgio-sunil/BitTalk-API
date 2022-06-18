
from __future__ import unicode_literals
import datetime
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from bit_talk_misc_api.static_models import Categories
from bit_talk_misc_api.serializers import CategoriesSerializer
from .serializers import CourseSerializer
from .models import Courses
from bit_talk_root.models import MongoUser
# from rest_framework.permissions import IsAuthenticated


class CoursesViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)

    # lookup_field = 'id'
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Courses.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        categories = instance.course_category
        for tag in instance.course_tags:
            new_category = Categories.objects(
                tags__iexact=tag,
                category_type__in=['All', 'Course'])
            review_category = Categories.objects.get(
                category_name__iexact='Review')
            if new_category.count() > 0:
                for c in new_category:
                    # Check if the category is already included?if not then add
                    if c not in categories:
                        if c != review_category:
                            categories.append(c)
        instance.course_category = categories
        instance.save()
        response = super().update(request, *args, **kwargs)
        return Response(response.data)

    @action(detail=True, methods=['patch'],
            url_path=r'start/(?P<user_id>[^/.]+)')
    def start_course(self, request, *args, **kwargs):
        course = self.get_object()
        user = MongoUser.objects.get(id=kwargs['user_id'])
        if course not in user.courses_started:
            user.courses_started.append(course)
            user.save()
            return Response({"message": "Course started successfully!"})
        return Response({"message": "Course already started!"})

    @action(detail=False, methods=['get'],
            url_path=r'academy')
    def get_academy(self, request, *args, **kwargs):
        start_time = datetime.datetime.now()
        data = {}
        qs = Courses.objects.all()
        if request.data.get('user_id') is not None:
            user_id = request.data['user_id']
            user_courses_serializer = CourseSerializer(
                        MongoUser.objects.get(id=user_id).courses_started,
                        many=True)
            data['user'] = user_courses_serializer.data

        course_serializer = CourseSerializer(
            qs,
            many=True)

        data['popular'] = course_serializer.data
        recent_serializer = CourseSerializer(
            qs.order_by('-course_date'),
            many=True)
        data['recent'] = recent_serializer.data

        categories_serializer = CategoriesSerializer(
            Categories.objects(category_type__in=['All', 'Course']),
            many=True)

        diff = datetime.datetime.now()-start_time
        msg = f"start_time = {start_time}, end_time = {datetime.datetime.now()}, difference in microseconds= {diff.microseconds}" # noqa
        data['categories'] = categories_serializer.data
        data['time_taken'] = msg
        return Response(data)
