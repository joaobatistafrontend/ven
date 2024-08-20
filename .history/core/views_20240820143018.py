from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *

class Index(View):
    template_name = 'index.html'
    def get(self, request):
        tipo_venda = TipoVenda.objects.all()
        todas_vendas = VendaDoProduto.objects.all()
        return render(request, self.template_name, {'todas_vendas':todas_vendas,'tipo_venda':tipo_venda})
    def post(self, request):
        tipo_venda_id = request.POST.get('tipo_venda')
            print(f"Tipo Venda ID: {tipo_venda_id}")  # Depuração

        tipo_venda = TipoVenda.objects.get(id=tipo_venda_id)

        # Redireciona para a nova venda com base no tipo de venda selecionado
        if tipo_venda.tipo == 'Entrega':
            form = VendaEntregaForm()
        elif tipo_venda.tipo == 'Retirada':
            form = VendaRetiradaForm()
        elif tipo_venda.tipo == 'Local':
            form = VendaLocalForm()

        return render(request, 'nova_venda.html', {'form': form, 'tipo_venda': tipo_venda})