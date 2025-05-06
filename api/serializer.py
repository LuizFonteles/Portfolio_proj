from rest_framework import serializers
import sys
sys.path.insert(0, '/home/luiz/proj/portfolio')
from portfolio.models import Stocks_symbols
from portfolio.models import Stocks_followed



class StockSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks_symbols
        fields = ['ticker']
