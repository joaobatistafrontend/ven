from django.shortcuts import render
from django.views.generic import View
from .models import *

class Index(View):
    template_name = 'index.html'
    def get(self, request):
        tipo_venda = TipoVenda.objects.all()
        todas_vendas = VendaDoProduto.objects.all()
        return render(request, self.template_name, {'todas_vendas':todas_vendas,'tipo_venda':tipo_venda})
        

