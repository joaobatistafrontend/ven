from django.urls import path
from .views import *
urlpatterns = [
    path('', Index.as_view(), name='index'),  # A rota raiz aponta para a view Index
]
