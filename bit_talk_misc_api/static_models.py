import datetime
from mongoengine import Document, EmbeddedDocument, fields


class ContentElement(EmbeddedDocument):
    content_title = fields.StringField()
    content_text = fields.StringField()


class StaticContent(Document):
    content_type = fields.StringField()
    content = fields.EmbeddedDocumentListField(ContentElement)


class ContactUs(Document):
    display_name = fields.StringField()
    email = fields.StringField()
    question = fields.StringField()


class Categories(Document):
    category_type = fields.StringField(default='All')
    category_name = fields.StringField(required=True, unique=True)
    category_image = fields.StringField(default="")
    tags = fields.ListField(fields.StringField(), unique=True)


class Languages(Document):
    locale = fields.StringField(required=True, unique=True)
    name = fields.StringField()
    image = fields.StringField(required=True)
    is_active = fields.BooleanField(default=True)
    string_file_url = fields.StringField()


class Banners(Document):
    Image = fields.StringField(required=True)
    Banner_title = fields.StringField(required=True)
    Banner_text = fields.StringField()
    Button_text = fields.StringField(required=True)
    Button_link = fields.StringField(required=True)
    Color_code = fields.StringField(required=True)
    is_active = fields.BooleanField(default=True)


class ModerationKeywords(Document):
    keyword = fields.StringField(required=True)
    reference = fields.StringField()
    time_published = fields.DateField(default=datetime.datetime.utcnow)
