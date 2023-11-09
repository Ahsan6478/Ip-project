from django.urls import include, path
from . import views

app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
]
