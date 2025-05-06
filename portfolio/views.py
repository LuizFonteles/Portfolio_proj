from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import AddStockForm, AlertRuleForm
from .models import AlertRule, Stocks_followed
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max



def fetch_stock_data(tickers):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token d9070e7e08ebae38639da21ddb761c8320b350ed',
    }
    url = f"https://api.tiingo.com/iex?tickers={",".join(tickers)}"
    print(url)
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json() 




@login_required
def follow_stock(request):
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.ticker = obj.ticker.upper()
            if Stocks_followed.objects.filter(user=request.user, ticker=obj.ticker).exists():
                messages.error(request, f"You’re already following “{obj.ticker}”.")
                return redirect('home')
            raw = fetch_stock_data([obj.ticker])
            if raw:
                data = raw[0]
                
                obj.timestamp = data["timestamp"]
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
                messages.error(request, f"Stock {obj.ticker} not found")
                return redirect('follow-stock')
    else:
        form = AddStockForm()
    return render(request, 'new_stock.html', { 'form': form })



@login_required
def list_alerts(request):
    rules = request.user.stocks_followed \
               .prefetch_related('alert_rules') \
               .values_list('alert_rules__id', flat=False)
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


@login_required
def delete_stock(request, pk):
    if request.user.is_authenticated:
        delete_it = get_object_or_404(Stocks_followed,pk=pk,user=request.user)
        if request.method == 'POST':
            delete_it.delete()
            messages.success(request, f"Stopped following {delete_it.ticker}")
        return redirect('home')

@login_required
def delete_alert(request, pk):
    if request.user.is_authenticated:
        delete_it = get_object_or_404(AlertRule, pk=pk, followed_stock__user=request.user)
        if request.method == 'POST':
            delete_it.delete()
            messages.success(request, "Alert deleted")
        return redirect('home')
    

