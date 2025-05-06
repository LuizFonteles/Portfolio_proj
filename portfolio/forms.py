from django import forms
from dal import autocomplete
from .models import AlertRule, Stocks_followed


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


class AlertRuleForm(forms.ModelForm):
    class Meta:
        model  = AlertRule
        fields = ['followed_stock', 'threshold', 'active','greater']
        widgets = {
            'followed_stock': forms.Select(attrs={'class': 'form-control'}),
            'threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'greater': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # only allow the user’s own followed stocks
            self.fields['followed_stock'].queryset = Stocks_followed.objects.filter(
                user=user
            )