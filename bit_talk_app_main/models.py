from djongo import models
from django.contrib.auth.models import AbstractUser
from mongoengine import Document, EmbeddedDocument, fields
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password

VISIBLE_CHOICES = [
    ('Everybody', 'Everybody'),
    ('Nobody', 'Nobody'),
    ('Selected', 'Selected')
]


class User(AbstractUser):

    gender = models.CharField(max_length=10, blank=True)
    preffered_lang = models.CharField(
                     max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_image = models.CharField(max_length=330, blank=True)
    preference = models.CharField(max_length=500, blank=True)
    profile_updated = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=False)
    posts_visible = models.CharField(
                    max_length=20, default="Everybody",
                    choices=VISIBLE_CHOICES)
    profile_photo_visible = models.CharField(
                    max_length=20, default="Everybody",
                    choices=VISIBLE_CHOICES)
    last_seen_online = models.CharField(
                    max_length=20, default="Everybody",
                    choices=VISIBLE_CHOICES)


# class MongoBaseUser():

#     # meta = {
#     #     'indexes': [
#     #         {'fields': ['username'], 'unique': True, 'sparse': True}
#     #     ]
#     # }

#     def set_password(self, raw_password):
#         """Sets the user's password - always use this rather than directly
#         assigning to :attr:`~mongoengine.django.auth.User.password` as the
#         password is hashed before storage.
#         """
#         self.password = make_password(raw_password)
#         self.save()
#         return self

#     def check_password(self, raw_password):
#         """Checks the user's password against a provided password - always use
#         this rather than directly comparing to
#         :attr:`~mongoengine.django.auth.User.password` as the password is
#         hashed before storage.
#         """
#         return check_password(raw_password, self.password)

#     @classmethod
#     def _create_user(cls, username, password, firstname=None, create_superuser=False):
#         """Create (and save) a new user with the given username, password and
#                 firstname address.
#                 """
#         now = timezone.now()

#         # Normalize the address by lowercasing the domain part of the email
#         # address.
#         try:
#             email_name, domain_part = username.strip().split('@', 1)
#         except ValueError:
#             pass
#         else:
#             username = '@'.join([email_name, domain_part.lower()])

#         user = cls(username=username, firstname=firstname, date_joined=now)
#         user.set_password(password)
#         user.save()
#         return user

#     @classmethod
#     def create_user(cls, username, password, firstname=None):
#         return cls._create_user(username, password, firstname)


# class MongoUser(Document):

#     username = fields.EmailField(
#                 verbose_name='e-mail address', unique=True, required=True)
#     first_name = fields.StringField(
#         max_length=30, blank=True, verbose_name='first name')
#     last_name = fields.StringField(
#         max_length=30, blank=True, verbose_name='last name')
#     password = fields.StringField(
#         max_length=128,
#         required=True,
#         verbose_name='password')
#     last_login = fields.DateTimeField(
#         default=timezone.now,
#         verbose_name='last login')
#     date_joined = fields.DateTimeField(
#         default=timezone.now,
#         verbose_name='date joined')


# class Coins(models.Model):
#     class Meta:
#         verbose_name_plural = "Coins"
#         ordering = ['-id']

#     cmc_id = models.IntegerField(blank=True)
#     symbol = models.CharField(max_length=50)
#     name = models.CharField(max_length=100)
#     logo = models.CharField(max_length=300)
#     active = models.BooleanField(default=True)


# class NewsFeed(models.Model):

#     class Meta:
#         verbose_name_plural = "NewsFeeds"
#         ordering = ['-id']

#     news_feed_url = models.CharField(max_length=300)
#     new_feed_short_name = models.CharField(max_length=50)
#     status = models.BooleanField(default=True)
