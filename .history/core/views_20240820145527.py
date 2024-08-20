from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from django.shortcuts import render
class Index(View):
    template_name = 'index.html'

    def get(self, request):
        tipo_venda = TipoVenda.objects.all()
        todas_vendas = Venda.objects.all()  # Use Venda para listar vendas
        return render(request, self.template_name, {'todas_vendas': todas_vendas, 'tipo_venda': tipo_venda})

    def post(self, request):
        tipo_venda_id = request.POST.get('tipo_venda')
        
        try:
            tipo_venda_id = int(tipo_venda_id)
        except (ValueError, TypeError):
            return redirect('index')

        tipo_venda = get_object_or_404(TipoVenda, id=tipo_venda_id)

        nova_venda = Venda.objects.create(tipo_venda=tipo_venda)

        if tipo_venda.tipo == 'Entrega':
            form = VendaEntregaForm(request.POST or None)
        elif tipo_venda.tipo == 'Retirada':
            form = VendaRetiradaForm(request.POST or None)
        elif tipo_venda.tipo == 'Local':
            form = VendaLocalForm(request.POST or None)

        if form.is_valid():
            dados = form.save(commit=False)
            dados.venda = nova_venda
            dados.save()
            return redirect('adicionar_produtos', venda_id=nova_venda.identificador_unico)

        return render(request, 'nova_venda.html', {'form': form, 'tipo_venda': tipo_venda})
    

    
    
    

class FinalizarVendaView(View):
    template_name = 'finalizar_venda.html'

    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        itens_venda = VendaDoProduto.objects.filter(venda=venda)
        return render(request, self.template_name, {'venda': venda, 'itens_venda': itens_venda})

    def post(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        # Lógica para finalizar a venda
        return redirect('resumo_venda', venda_id=venda.identificador_unico)