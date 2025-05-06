from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Stocks_symbols(models.Model):
    ticker = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return self.ticker

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio_name = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
class Stocks_followed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='stocks_followed')
#    ticker = models.ForeignKey(Stocks_symbols, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    open = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)
    mid = models.FloatField(null=True, blank=True)
    tngolast = models.FloatField(null=True, blank=True)
    prevClose = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'ticker'],
                                    name='unique_user_ticker')
        ]

    def __str__(self):
        return f"{self.ticker}"
    

class AlertRule(models.Model):
    followed_stock = models.ForeignKey(
        Stocks_followed,
        on_delete=models.CASCADE,
        related_name='alert_rules'
    )
    threshold = models.FloatField(help_text="Notify when price falls below this")
    active = models.BooleanField(default=True)
    sleeping = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    greater = models.BooleanField(default=False)

    def __str__(self):
        # show the ticker and threshold
        if not self.greater:
            return f"{self.followed_stock.ticker} < {self.threshold}"
        if self.greater:
            return f"{self.followed_stock.ticker} > {self.threshold}"