from django.urls import path
from .views import *
urlpatterns = [
    path('', Index.as_view(), name='index'),  # A rota raiz aponta para a view Index
    path('adicionar_produtos/<int:venda_id>/', AdicionarProdutosView.as_view(), name='adicionar_produtos'),
    path('finalizar_venda/<int:venda_id>/', FinalizarVenda.as_view(), name='finalizar_venda'),
]
