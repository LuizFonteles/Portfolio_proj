# portfolio/autocomplete.py
#from dal import autocomplete
#from .models import Stocks_symbols



#class StockSymbolAutocomplete(autocomplete.Select2QuerySetView):
#    def get_queryset(self):
#        if not self.q:
#            return Stocks_symbols.objects.none()

#        return Stocks_symbols.objects.filter(
#            ticker__icontains=self.q
#        ).order_by('ticker')[:20]

