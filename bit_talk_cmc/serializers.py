# from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import CmcCoinsList, Coins


class CmcCoinsSerializer(DocumentSerializer):
    # id = serializers.CharField(read_only=False)

    class Meta:
        model = CmcCoinsList
        fields = '__all__'
        depth = 1


class CoinsSerializer(DocumentSerializer):
    # id = serializers.CharField(read_only=False)

    class Meta:
        model = Coins
        fields = '__all__'
        depth = 1
