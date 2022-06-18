from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .models import Coins


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Authentication POST succeded!!"})
    return Response({"message": "Hello World"})


@api_view(['GET'])
def get_coins_latest(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
        }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.COIN_API_KEY,
        }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        return Response(response.json())
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


@api_view(['GET'])
def get_coins_list(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    cmc_id_list = []
    for coin in Coins.objects.filter(active__in=[True]):
        cmc_id_list.append(coin.cmc_id)

    parameters = {
        'id': ",".join(str(x) for x in cmc_id_list)
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.COIN_API_KEY,
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        return Response(response.json())
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


@api_view(['GET'])
def get_coins_ohlcv_historic(request):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'  # noqa
    cmc_id_list = []
    for coin in Coins.objects.filter(active__in=[True]):
        cmc_id_list.append(coin.cmc_id)

    parameters = {
        'id': ",".join(str(x) for x in cmc_id_list)
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.COIN_API_KEY,
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        api_response = Response(response.json())
        for rec in api_response.data['data']:
            logo = F"https://s2.coinmarketcap.com/static/img/coins/64x64/{rec}.png",  # noqa
            api_response.data['data'][rec]['logo'] = logo
        return api_response
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
