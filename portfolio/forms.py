from django import forms
from dal import autocomplete
from .models import Stocks_followed
from .models import Stocks_symbols


class AddStockForm(forms.ModelForm):
    ticker = forms.CharField(
        max_length=20,
        label="Ticker Symbol",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. AAPL',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Stocks_followed
        fields = ['ticker']