from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Stocks_symbols(models.Model):
    ticker = models.CharField(primary_key=True, max_length=10)


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
class Stocks_followed(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Stocks_symbols, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    mid = models.FloatField()
    tngolast = models.FloatField()
    prevClose = models.FloatField()
    volume = models.FloatField()


    def __str__(self):
        return f"{self.stock_symbol}"
    
