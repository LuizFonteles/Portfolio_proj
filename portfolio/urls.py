from django.urls import path
from .views import follow_stock
#from .autocomplete import StockSymbolAutocomplete

urlpatterns = [
    path('', follow_stock, name='follow-stock'),
#    path(
#        'stocksymbol-autocomplete/',StockSymbolAutocomplete.as_view(),name='stocksymbol-autocomplete'
#        ),
]