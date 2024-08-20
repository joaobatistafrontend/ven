# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('nova-venda/', NovaVenda.as_view(), name='nova_venda'),
    path('adicionar_produtos/<int:venda_id>/', AdicionarProdutosView.as_view(), name='adicionar_produtos'),
    # Adicione a URL para 'resumo_venda' aqui, se necessário
]
