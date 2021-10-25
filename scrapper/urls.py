
from django.urls import path
from .views import MAIN

urlpatterns = [
    path('', MAIN.as_view(), name='main')
]