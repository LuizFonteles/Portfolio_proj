from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .serializer import StockSymbolSerializer, StocksSerializer



@api_view(['GET'])
def getStockSymbols(request):
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token d9070e7e08ebae38639da21ddb761c8320b350ed',
    }
    requestResponse = requests.get("https://api.tiingo.com/iex", headers=headers)
    requestResponse.raise_for_status()
    raw = requestResponse.json()
    tickers_list = []
    for item in raw:
        tickers_list.append({'ticker': item['ticker']})
    serializer = StockSymbolSerializer(data=tickers_list, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def getStocks(request, stocks):
    print("wow")
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token d9070e7e08ebae38639da21ddb761c8320b350ed',
    }
    requestResponse = requests.get(f"https://api.tiingo.com/iex?tickers={",".join(stocks)}" , headers=headers)
    raw = requestResponse.json()
    stocks_data = [{'timestamp': item['timestamp'],
                    'high': item['high'],
                    'open': item['open'],
                    'low': item['low'],
                    'mid': item['mid'],
                    'tngolast': item['tngoLast'],
                    'prevClose': item['prevClose'],
                    'volume': item['volume'],
                    } 
                    for item in raw
                    ]
    serializer = StocksSerializer(data=stocks_data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save(commit=False)
    print(serializer.data)
    return serializer.validated_data
