# from builtins import ValueError, classmethod
from django.utils import timezone
# from django.contrib.auth.hashers import check_password, make_password
from mongoengine import Document, fields
from bit_talk_app_course.models import Courses

VISIBLE_CHOICES = (
    ('Everybody', 'Everybody'),
    ('Nobody', 'Nobody'),
    ('Selected', 'Selected')
)


# class MongoBaseUser():

#     meta = {
#         'indexes': [
#             {'fields': ['username'], 'unique': True, 'sparse': True}
#         ]
#     }

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


class MongoUser(Document):

    username = fields.EmailField(
        verbose_name='e-mail address', unique=True, required=True)
    first_name = fields.StringField(blank=True, verbose_name='first name')
    last_name = fields.StringField(blank=True, verbose_name='last name')
    password = fields.StringField(required=True, verbose_name='password')
    gender = fields.StringField()
    preffered_lang = fields.StringField()
    dob = fields.DateField()
    country = fields.StringField()
    profile_image = fields.StringField()
    preference = fields.ListField(fields.StringField())
    profile_updated = fields.BooleanField(default=False)
    push_notifications = fields.BooleanField(default=False)
    email_notifications = fields.BooleanField(default=False)
    posts_visible = fields.StringField(
        choices=VISIBLE_CHOICES, default='Everybody')
    profile_photo_visible = fields.StringField(
        choices=VISIBLE_CHOICES, default='Everybody')
    last_seen_online = fields.StringField(
        choices=VISIBLE_CHOICES, default='Everybody')
    last_login = fields.DateTimeField(
        default=timezone.now, verbose_name='last login')
    date_joined = fields.DateTimeField(
        default=timezone.now, verbose_name='date joined')
    courses_started = fields.ListField(fields.ReferenceField(Courses))
