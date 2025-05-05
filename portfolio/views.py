from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import AddStockForm
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
