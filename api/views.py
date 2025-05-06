from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .serializer import StockSymbolSerializer



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
