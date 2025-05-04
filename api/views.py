from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

@api_view(['GET'])
def getData(request):
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token d9070e7e08ebae38639da21ddb761c8320b350ed',
    }
    requestResponse = requests.get("https://api.tiingo.com/iex", headers=headers)
    return Response(requestResponse)