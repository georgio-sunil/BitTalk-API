from mongoengine import Document, EmbeddedDocument, fields
# from bit_talk_app_main.models import User
# from django_mongoengine.mongo_auth.models import User
from bit_talk_misc_api.static_models import Categories
from bson.objectid import ObjectId
from bit_talk_root.models import MongoUser

STATUS_CHOICES = [
    ('New', 'New'),
    ('Flagged', 'Flagged'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Reported', 'Reported'),
    ('Passed', 'Passed')
]


class NewsFeed(Document):

    news_feed_url = fields.StringField(unique=True)
    new_feed_short_name = fields.StringField()
    status = fields.BooleanField(default=True)


class Comments(EmbeddedDocument):
    id = fields.ObjectIdField(required=True, default=ObjectId)
    comment_text = fields.StringField(required=True)
    user_ref = fields.ReferenceField(MongoUser)
    status = fields.StringField(required=True, default='New', choices=STATUS_CHOICES)
    time_stamp = fields.DateTimeField()
    reported_flag = fields.BooleanField(default=False)
    reported_reason = fields.StringField()
    reported_count = fields.IntField(default=0)


class News_articles(Document):
    # id = fields.StringField(required=True, primary_key=True)
    news_title = fields.StringField(required=True, unique=True)
    news_link = fields.StringField()
    time_published = fields.DateField()
    author = fields.StringField()
    tags = fields.ListField(fields.StringField())
    summary = fields.StringField()
    content = fields.StringField()
    img = fields.StringField()
    source = fields.StringField()
    comments = fields.EmbeddedDocumentListField(Comments)
    category = fields.ListField(fields.ReferenceField(Categories))
    no_of_views = fields.IntField(default=0)
    no_of_likes = fields.IntField(default=0)
    no_of_comments = fields.IntField(default=0)
    no_of_shares = fields.IntField(default=0)
    liked_by = fields.ListField(fields.ReferenceField(MongoUser))
