from django.db import models

# Create your models here.

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
