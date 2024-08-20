from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from django.shortcuts import render
from decimal import Decimal

class Index(View):
    template_name = 'index.html'

    def get(self, request):
        tipo_venda = TipoVenda.objects.all()
        todas_vendas = VendaDoProduto.objects.all()
        return render(request, self.template_name, {'todas_vendas': todas_vendas, 'tipo_venda': tipo_venda})

    def post(self, request):
        tipo_venda_id = request.POST.get('tipo_venda')
        
        try:
            tipo_venda_id = int(tipo_venda_id)
        except (ValueError, TypeError):
            return redirect('index')

        tipo_venda = get_object_or_404(TipoVenda, id=tipo_venda_id)

        # Cria uma nova venda com o tipo selecionado
        nova_venda = Venda.objects.create(tipo_venda=tipo_venda)

        # Define o formulário baseado no tipo de venda
        if tipo_venda.tipo == 'Entrega':
            form = VendaEntregaForm(request.POST or None)
        elif tipo_venda.tipo == 'Retirada':
            form = VendaRetiradaForm(request.POST or None)
        elif tipo_venda.tipo == 'Local':
            form = VendaLocalForm(request.POST or None)

        return render(request, 'nova_venda.html', {'form': form, 'tipo_venda': tipo_venda})
    
class NovaVenda(View):
        template_name = 'index.html'

    def get(self, request):
        tipo_venda = TipoVenda.objects.all()
        todas_vendas = VendaDoProduto.objects.all()
        return render(request, self.template_name, {'todas_vendas': todas_vendas, 'tipo_venda': tipo_venda})




class AdicionarProdutosView(View):
    template_name = 'adicionar_produtos.html'

    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        produtos = Produto.objects.all()
        return render(request, self.template_name, {'venda': venda, 'produtos': produtos})

    def post(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade'))

        produto = get_object_or_404(Produto, id=produto_id)

        total = produto.valor * Decimal(quantidade)

        item_venda, created = VendaDoProduto.objects.get_or_create(
            venda=venda,
            produto=produto,
            defaults={'qtd': quantidade, 'total': total}
        )
        
        if not created:
            item_venda.qtd += quantidade
            item_venda.total = item_venda.qtd * produto.valor
            item_venda.save()

        return redirect('adicionar_produtos', venda_id=venda.identificador_unico)
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