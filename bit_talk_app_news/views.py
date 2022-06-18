import datetime
import feedparser
import re
from dateutil import parser
from html.parser import HTMLParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import (
    NewsSerializer,
    NewsTagsSerializer,
    NewsCommentsSerializer,
    NewsFeedSerializer)
from .models import News_articles, Comments, NewsFeed, STATUS_CHOICES
from bit_talk_misc_api.static_models import Categories
from profanity_filter import ProfanityFilter
from bson.objectid import ObjectId


class NewsFeedViewSet(ModelViewSet):
    serializer_class = NewsFeedSerializer

    def get_queryset(self):
        return NewsFeed.objects.all()


class NewsViewSet(ModelViewSet):

    serializer_class = NewsSerializer

    def get_queryset(self):
        return News_articles.objects.all()

    @action(detail=True, methods=['patch'], url_path=r'tags',)
    def update_tags(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NewsTagsSerializer(data=request.data)
        if serializer.is_valid():
            for tag in serializer.validated_data['tags']:
                # Check if the tag is already present, if not then add
                if tag not in instance.tags:
                    instance.tags.append(tag)
                    instance.save()
            self.assign_category(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path=r'comments',)
    def add_comment(self, request, *args, **kwargs):
        pf = ProfanityFilter()
        instance = self.get_object()
        status = 'New'
        serializer = NewsCommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data['comments']
        for comment in serializer.validated_data['comments']:
            raw_comment = comment['comment_text']
            if (pf.is_profane(raw_comment)):
                status = 'Flagged'
            c = Comments(
                comment_text=raw_comment,  # pf.censor(raw_comment),
                status=status,
                user_ref=comment['user_ref'],
                time_stamp=datetime.datetime.now)
            instance.comments.append(c)
            instance.no_of_comments += 1
            instance.save()
        return Response(serializer.data)

    @action(detail=True, methods=['patch'],
            url_path=r'report_comment/(?P<comment_id>[^/.]+)')
    def report_comment(self, request, *args, **kwargs):
        reported_reason = request.data.get('reported_reason')
        reported_count = request.data.get('reported_count')

        try:
            News_articles.objects(
                                 __raw__={'comments.id': ObjectId(kwargs['comment_id'])}  # noqa : E501
                                 ).update(
                                 __raw__={'$set': {'comments.$.reported_reason': reported_reason,  # noqa : E501
                                                   'comments.$.reported_count': reported_count,  # noqa : E501
                                                   'comments.$.reported_flag': True}})  # noqa : E501
        except Exception:
            return Response({'message': 'Some error occoured!'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Comment reported!'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'],
            url_path=r'update_comment_status/(?P<comment_id>[^/.]+)')
    def update_comment_status(self, request, *args, **kwargs):
        comment_status = request.data.get('status')
        try:
            if comment_status in dict(STATUS_CHOICES):
                News_articles.objects(
                                    __raw__={'comments.id': ObjectId(kwargs['comment_id'])}  # noqa : E501
                                    ).update(
                                    __raw__={'$set': {'comments.$.status': comment_status}})  # noqa : E501
            else:
                return Response({'message': 'Invalid status!'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as err:
            return Response({'message': err},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Status updated!'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'],
            url_path=r'like/(?P<user_id>[^/.]+)')
    def add_like(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if kwargs['user_id'] not in instance.liked_by:
            instance.liked_by.append(kwargs['user_id'])
            instance.no_of_likes += 1
            instance.save()
        return Response(serializer.data)

    def assign_category(instance):   # def assign_category(self, request):
        categories = instance.category
        for tag in instance.tags:
            new_category = Categories.objects(
                tags__iexact=tag,
                category_type__in=['All', 'News'])
            review_category = Categories.objects.get(
                category_name__iexact='Review')
            if new_category.count() > 0:
                for c in new_category:
                    # Check if the category is already included?if not then add
                    if c not in categories:
                        if c != review_category:
                            categories.append(c)
            else:
                category_review = Categories.objects.get(
                    category_name='Review')
                category_review.tags.append(tag)
                category_review.save()
        instance.category = categories
        instance.save()

    @action(detail=False, methods=['get'], url_path=r'fetch-from-active-feeds')
    def fetch_news_from_feeds(self, request):
        count = 0
        feeds_list = NewsFeed.objects(status__in=[True])
        msg = ""
        for feed in feeds_list:
            response = get_news_btc(
                feed.news_feed_url,
                feed.new_feed_short_name)
            msg = msg + f"Added {response.data['count']} new article(s) from {feed.new_feed_short_name}, "  # noqa
            count += response.data['count']
        return Response({"msg": msg, "total": count})


class parse_img(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = ""
        self.capture = False

    def handle_starttag(self, tag, attrs):
        search_list = [index for (index, a_tuple) in enumerate(attrs) if a_tuple[0] == "src"]  # noqa
        if len(search_list) == 1:
            index = search_list[0]
            if attrs[index][0] == 'src':
                self.capture = True
                self.data = attrs[index][1]


def get_news_btc(feed_url, source):
    # feed_url = 'https://www.btcwires.com/feed/'
    news_feed = feedparser.parse(feed_url)
    # articles_list = []
    article_count = 0
    pattern = '<img.*/>'
    for article in news_feed.entries:
        temp = dict()
        temp["title"] = article.get('title', 'No title from feed')
        temp["link"] = article.get('link', 'No link')
        temp["author"] = article.get('author', 'No author')
        temp["time_published"] = article.get('published', datetime.datetime.today())  # noqa
        temp["tags"] = []
        if article.has_key('tags'):  # noqa
            temp["tags"] = [tag.term for tag in article.tags]
        temp["authors"] = []
        if article.has_key('authors'):  # noqa
            temp["authors"] = [author.name for author in article.authors]
        temp["summary"] = article.get('summary', 'No Summary')
        temp["img"] = "No Img from feed"
        result = re.findall(pattern, article.content[0].value)
        if len(result) == 1:
            myparser = parse_img()
            myparser.feed(result[0])
            if myparser.capture:
                temp["img"] = myparser.data
        temp["content"] = re.sub(pattern, "", article.content[0].value)
        """
        Check if article by this title already exists
        """
        qs = News_articles.objects.filter(news_title__contains=article.title)
        if qs.count() == 0:
            news_article = News_articles(
                            news_title=temp["title"],
                            news_link=temp["link"],
                            time_published=parser.parse(temp["time_published"]),  # noqa
                            tags=temp["tags"],
                            img=temp["img"],
                            content=temp["content"],
                            summary=temp["summary"],
                            author=temp["author"],
                            source=source
                            )
            news_article.save()
            article_count += 1
            NewsViewSet.assign_category(news_article)
            # articles_list.append(temp)
    # json_news["articles"] = articles_list
    # msg = f"Added {len(articles_list)} new article(s)."
    # response = json_news  # json.dumps(json_news)
    # return Response(response)
    return Response({"count": article_count})
