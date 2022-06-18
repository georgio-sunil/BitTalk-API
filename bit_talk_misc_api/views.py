from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
                         EmailSubscribeSerializer,
                         StaticContentSerializer,
                         ContactUsSerializer,
                         CategoriesSerializer,
                         LanguagesSerializer,
                         BannersSerializer,
                         ModerationKeywordsSerializer)

from .models import EmailSubscribe
from .static_models import (
                            StaticContent,
                            ContactUs,
                            Categories,
                            Languages,
                            Banners,
                            ModerationKeywords)
from bit_talk_app_course.models import Courses
from bit_talk_app_course.serializers import CourseSerializer
from bit_talk_app_news.models import News_articles
from bit_talk_app_news.serializers import NewsSerializer


class SubscribeList(generics.ListCreateAPIView):
    lookup_field = 'email'
    permission_classes = (AllowAny,)
    queryset = EmailSubscribe.objects.all()
    serializer_class = EmailSubscribeSerializer


class SubscribeDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'email'
    queryset = EmailSubscribe.objects.all()
    serializer_class = EmailSubscribeSerializer


class StaticContentViewSet(ModelViewSet):
    serializer_class = StaticContentSerializer

    def get_queryset(self):
        return StaticContent.objects.all()


class ContactUsViewSet(ModelViewSet):
    serializer_class = ContactUsSerializer

    def get_queryset(self):
        return ContactUs.objects.all()


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return Categories.objects.all()

    @action(detail=True, methods=['get'], url_path=r'courses',)
    def get_courses(self, request, *args, **kwargs):
        instance = self.get_object()
        courses = Courses.objects(course_category=instance)
        course_serializer = CourseSerializer(courses, many=True)
        return Response(course_serializer.data)

    @action(detail=True, methods=['get'], url_path=r'news',)
    def get_news(self, request, *args, **kwargs):
        instance = self.get_object()
        news = News_articles.objects(category=instance)
        course_serializer = NewsSerializer(news, many=True)
        return Response(course_serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     queryset_courses = queryset.filter(category_type__iexact='course')

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(
    #             {"data": serializer.data,
    #              "total_categories_count": len(queryset),
    #              "total_course_count": len(queryset_courses)})


class LanguagesViewSet(ModelViewSet):
    serializer_class = LanguagesSerializer

    def get_queryset(self):
        return Languages.objects.all()


class BannersViewSet(ModelViewSet):
    serializer_class = BannersSerializer

    def get_queryset(self):
        return Banners.objects.all()


class ModerationKeywordViewSet(ModelViewSet):
    serializer_class = ModerationKeywordsSerializer

    def get_queryset(self):
        return ModerationKeywords.objects.all()
