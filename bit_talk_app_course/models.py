
import datetime
from mongoengine import Document, EmbeddedDocument, fields
from bit_talk_misc_api.static_models import Categories
from bson.objectid import ObjectId


class Topics(EmbeddedDocument):
    id = fields.ObjectIdField(required=True, default=ObjectId)
    topic_name = fields.StringField(required=True)
    topic_desc = fields.StringField(required=True)
    topic_type = fields.StringField(required=True)
    topic_image = fields.StringField(required=True)
    topic_url = fields.StringField()
    topic_content = fields.StringField()
    topic_date = fields.DateTimeField(default=datetime.datetime.utcnow)


class Courses(Document):
    course_name = fields.StringField(required=True, unique=True)
    course_desc = fields.StringField(required=True)
    course_tags = fields.ListField(fields.StringField())
    course_image = fields.StringField()
    course_url = fields.StringField()
    course_date = fields.DateTimeField(default=datetime.datetime.utcnow)
    course_category = fields.ListField(fields.ReferenceField(Categories))
    topic_count = fields.IntField(default=0)
    video_count = fields.IntField(default=0)
    course_bg = fields.StringField()
    topics = fields.EmbeddedDocumentListField(Topics)
