from django.urls import path
from .views import Home, About

urlpatterns = [
    path('', Home), #localhost:8000
    path('about/', About), # localhost:8000/about
]