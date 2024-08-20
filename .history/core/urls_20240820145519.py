# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('adicionar_produtos/<int:venda_id>/', AdicionarProdutosView.as_view(), name='adicionar_produtos'),
    path('finalizar_venda/<int:venda_id>/', FinalizarVendaView.as_view(), name='finalizar_venda'),
    # Adicione a URL para 'resumo_venda' aqui, se necessário
]
