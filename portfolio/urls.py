from django.urls import path
from .views import follow_stock, list_alerts, create_or_edit_alert
#from .autocomplete import StockSymbolAutocomplete

urlpatterns = [
    path('', follow_stock, name='follow-stock'),
    path('alerts/', list_alerts, name='alert-list'),
    path('alerts/new/', create_or_edit_alert, name='alert-create'),
    path('alerts/<int:pk>/edit/', create_or_edit_alert, name='alert-edit'),
#    path(
#        'stocksymbol-autocomplete/',StockSymbolAutocomplete.as_view(),name='stocksymbol-autocomplete'
#        ),
]