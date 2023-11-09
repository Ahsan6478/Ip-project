from django.db import models
from django.contrib import admin


class User(models.Model):
    options = (
        ('blocked', "Blocked"),
        ("unblock", 'Unblock')
    )
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=30)
    req_count = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=options, default='unblock')
    unblock_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.name 
    
    class Meta:
        ordering = ("-req_count",)
        
    