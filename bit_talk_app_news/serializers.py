from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import News_articles, NewsFeed


class NewsFeedSerializer(DocumentSerializer):

    class Meta:
        model = NewsFeed
        fields = '__all__'
        depth = 1


class NewsSerializer(DocumentSerializer):

    class Meta:
        model = News_articles
        fields = '__all__'
        depth = 2


class NewsTagsSerializer(DocumentSerializer):

    class Meta:
        model = News_articles
        fields = ['tags']
        depth = 2


class NewsCommentsSerializer(DocumentSerializer):

    class Meta:
        model = News_articles
        fields = ['comments']
        depth = 2
