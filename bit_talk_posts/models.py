from mongoengine import Document, fields
from bit_talk_app_news.models import Comments, STATUS_CHOICES
from bit_talk_root.models import MongoUser
from bit_talk_cmc.models import Coins

# STATUS_CHOICES = [
#     ('New', 'New'),
#     ('Flagged', 'Flagged'),
#     ('Approved', 'Approved'),
#     ('Rejected', 'Rejected')
# ]


class Posts(Document):
    content = fields.StringField(required=True)
    image = fields.StringField()
    post_status = fields.StringField(default= 'New', choices=STATUS_CHOICES)
    trending_flag = fields.BooleanField(default=False)
    no_of_views = fields.IntField(default=0)
    no_of_likes = fields.IntField(default=0)
    no_of_comments = fields.IntField(default=0)
    no_of_shares = fields.IntField(default=0)
    reported_flag = fields.BooleanField(default=False)
    reported_reason = fields.StringField()
    reported_count = fields.IntField(default=0)
    # reported_by = fields.ReferenceField(MongoUser)
    user_ref = fields.ReferenceField(MongoUser, reverse_delete_rule='CASCADE')
    liked_by = fields.ListField()
    post_coin_ref = fields.ListField(fields.ReferenceField(Coins))
    comments = fields.EmbeddedDocumentListField(Comments)
