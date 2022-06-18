from __future__ import unicode_literals
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from .serializers import CmcCoinsSerializer, CoinsSerializer
from .models import CmcCoinsList
from bit_talk_cmc.models import Coins
from rest_framework.decorators import action
import coinmarketcapapi


class CoinsViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)

    serializer_class = CoinsSerializer

    def get_queryset(self):
        return Coins.objects.all()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        coin = self.get_object()
        if request.data.get('active') is False:
            response = CmcCoinsList.objects.filter(
                cmc_id=str(coin.cmc_id)).delete()
        response = super().update(request, *args, **kwargs)
        return response


class CmcCoinsViewSet(ModelViewSet):
    serializer_class = CmcCoinsSerializer
    cmc = coinmarketcapapi.CoinMarketCapAPI(settings.COIN_API_KEY)

    def get_queryset(self):
        return CmcCoinsList.objects.all()

    @action(detail=False, methods=['get'], url_path=r'fetch',)
    def fetch_coins_info(self, request, *args, **kwargs):
        qs_coins = Coins.objects.filter(active__in=[True])
        cms_ids = [i.cmc_id for i in qs_coins]
        for cmc_id in cms_ids:
            if CmcCoinsList.objects.filter(cmc_id=cmc_id).count() == 0:
                info_data = self.cmc.cryptocurrency_info(id=cmc_id)
                coin_entry = {}
                coin_entry['cmc_id'] = info_data.data[str(cmc_id)]['id']
                coin_entry['logo'] = info_data.data[str(cmc_id)]['logo']
                coin_entry['name'] = info_data.data[str(cmc_id)]['name']
                coin_entry['symbol'] = info_data.data[str(cmc_id)]['symbol']
                coin_entry['about'] = info_data.data[str(
                    cmc_id)]['description']
                serializer = self.get_serializer(data=coin_entry)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path=r'refresh',)
    def update_coins_info(self, request, *args, **kwargs):
        id = ''
        interval = 'hourly'
        time_period = 'hourly'
        time_start = '2022-05-24T13:00'
        time_end = '2022-05-25T13:45'
        qs = self.get_queryset()
        id = ",".join(str(x.cmc_id) for x in qs)
        ohlcv_info = self.cmc.cryptocurrency_ohlcv_historical(
            id=id, interval=interval,
            time_period=time_period,
            time_start=time_start,
            time_end=time_end)
        latest_info = self.cmc.cryptocurrency_quotes_latest(
            id=id)
        for coin in qs:
            coin.quotes_24h = ohlcv_info.data[coin.cmc_id]['quotes']
            coin.price_usd = latest_info.data[coin.cmc_id]['quote']['USD']['price']
            coin.percentage_change_24h = latest_info.data[coin.cmc_id]['quote']['USD']['percent_change_24h']
            coin.percentage_change_7d = latest_info.data[coin.cmc_id]['quote']['USD']['percent_change_7d']
            coin.percentage_change_30d = latest_info.data[coin.cmc_id]['quote']['USD']['percent_change_30d']
            coin.percentage_change_60d = latest_info.data[coin.cmc_id]['quote']['USD']['percent_change_60d']
            coin.percentage_change_90d = latest_info.data[coin.cmc_id]['quote']['USD']['percent_change_90d']
            coin.market_cap = latest_info.data[coin.cmc_id]['quote']['USD']['market_cap']
            coin.circulation_supply = latest_info.data[coin.cmc_id]['circulating_supply']
            coin.total_supply = latest_info.data[coin.cmc_id]['total_supply']
            coin.save()
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
