from django.urls import path
from .views import Home, About

urlpatterns = [
    path('', Home, name='home'), #localhost:8000
    path('about/', About, name='about'), # localhost:8000/about
]