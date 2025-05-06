from django.conf import settings
import requests
from .models import Stocks_followed, AlertRule
from django.core.mail import send_mail


def make_request():
    TIINGO_URL = "https://api.tiingo.com/iex?tickers={tickers}"
    tickers = list(
            Stocks_followed.objects.values_list('ticker', flat=True).distinct()
        )
                
    if not tickers:
        return "No tickers to update"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token d9070e7e08ebae38639da21ddb761c8320b350ed',
    }
    response = requests.get(
        TIINGO_URL.format(tickers=",".join(tickers)),
        headers=headers
    )
    response.raise_for_status()
    raw = response.json() 
    
    return raw


def update_stocks(data_map):
    updated = 0
    for sf in Stocks_followed.objects.all():
        data = data_map.get(sf.ticker)
        if not data:
            continue
        sf.open      = data['open']
        sf.high      = data['high']
        sf.low       = data['low']
        sf.mid       = data.get('mid')
        sf.tngolast  = data['tngoLast']
        sf.prevClose = data['prevClose']
        sf.volume    = data['volume']
        sf.timestamp = data['timestamp']
        sf.save(update_fields=[
            'open','high','low','mid','tngolast','prevClose','volume','timestamp'
        ])
        updated += 1
    return updated


def check_alerts(data_map):
    for rule in AlertRule.objects.filter(active=True, sleeping=False):
        ticker = rule.followed_stock.ticker
        data = data_map.get(ticker)  
        price = data['tngoLast']
        
        # If price is below the user’s threshold, send email
        if price is not None:
            if not rule.greater and  price < rule.threshold:
                user = rule.followed_stock.user
                subject = f"[StockViewer] Alert: {ticker} at {price:.2f}"
                message = (
                    f"Hello {user.username},\n\n"
                    f"The stock {ticker} has dropped to {price:.2f},\n"
                    f"which is below your alert threshold of {rule.threshold:.2f}.\n\n"
                    "Log in to view your other alerts"
                    "Regards,\n"
                    "Stock follower"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            elif rule.greater and price > rule.threshold:
                user = rule.followed_stock.user
                subject = f"[StockViewer] Alert: {ticker} at {price:.2f}"
                message = (
                    f"Hello {user.username},\n\n"
                    f"The stock {ticker} has risen to {price:.2f},\n"
                    f"which is above your alert threshold of {rule.threshold:.2f}.\n\n"
                    "Log in to view your other alerts"
                    "Regards,\n"
                    "Stock follower"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            rule.sleeping = True
            rule.save(update_fields=['sleeping'])

    for rule in AlertRule.objects.filter(active=True, sleeping=True):
        ticker = rule.followed_stock.ticker
        data = data_map.get(ticker) 
        price = data['tngoLast']

        if price is not None:
            if not rule.greater and  price > rule.threshold:
                rule.sleeping = False
                rule.save(update_fields=['sleeping'])

            elif rule.greater and  price < rule.threshold:
                rule.sleeping = False
                rule.save(update_fields=['sleeping'])      