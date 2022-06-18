from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import EmailSubscribe
from .static_models import (StaticContent,
                            ContactUs,
                            Categories,
                            Languages,
                            Banners,
                            ModerationKeywords)


class EmailSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscribe
        fields = '__all__'
        lookup_field = 'email'


class StaticContentSerializer(DocumentSerializer):

    class Meta:
        model = StaticContent
        fields = '__all__'
        depth = 2


class ContactUsSerializer(DocumentSerializer):

    class Meta:
        model = ContactUs
        fields = '__all__'
        depth = 1


class CategoriesSerializer(DocumentSerializer):

    class Meta:
        model = Categories
        fields = '__all__'
        depth = 1


class LanguagesSerializer(DocumentSerializer):

    class Meta:
        model = Languages
        fields = '__all__'
        depth = 1


class BannersSerializer(DocumentSerializer):

    class Meta:
        model = Banners
        fields = '__all__'
        depth = 1

        
class ModerationKeywordsSerializer(DocumentSerializer):

    class Meta:
        model = ModerationKeywords
        fields = '__all__'
        depth = 1
