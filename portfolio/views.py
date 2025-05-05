from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import AddStockForm, AlertRuleForm
from .models import AlertRule
from api.views import getStocks
import requests

def fetch_stock_data(tickers):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token d9070e7e08ebae38639da21ddb761c8320b350ed',
    }
    url = f"https://api.tiingo.com/iex?tickers={",".join(tickers)}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json() 




@login_required
def follow_stock(request):
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            raw = fetch_stock_data(obj.ticker)
            data = raw[0]
            
            obj.timestamp = timezone.now()
            obj.open = data["open"]
            obj.high = data["high"]
            obj.low = data["low"]
            obj.mid = data["mid"]
            obj.tngolast = data["tngoLast"]
            obj.prevClose = data["prevClose"]
            obj.volume = data["volume"]
            
            obj.save()
            messages.success(request, f"Now following {obj.ticker}")
            return redirect('home')
    else:
        form = AddStockForm()
    return render(request, 'new_stock.html', { 'form': form })



@login_required
def list_alerts(request):
    # fetch only this user’s rules
    rules = request.user.stocks_followed \
               .prefetch_related('alert_rules') \
               .values_list('alert_rules__id', flat=False)
    # simpler: directly
    rules = AlertRule.objects.filter(followed_stock__user=request.user)
    return render(request, 'alert_list.html', {'rules': rules})

@login_required
def create_or_edit_alert(request, pk=None):
    if pk:
        rule = get_object_or_404(
            AlertRule, pk=pk, followed_stock__user=request.user
        )
    else:
        rule = None

    if request.method == 'POST':
        form = AlertRuleForm(request.POST, instance=rule, user=request.user)
        if form.is_valid():
            alert = form.save()
            messages.success(request, "Alert saved.")
            return redirect('alert-list')
    else:
        form = AlertRuleForm(instance=rule, user=request.user)

    return render(request, 'alert_form.html', {'form': form})

