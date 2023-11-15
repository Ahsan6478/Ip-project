# urls.py

from django.urls import path
from .views import ChargeCardAPIView

app_name = "payment"
urlpatterns = [
    path('charge/', ChargeCardAPIView.as_view(), name='charge-card'),
]
