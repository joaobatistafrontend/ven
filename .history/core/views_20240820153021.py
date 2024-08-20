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
    template_name = 'nova_venda.html'

    def get(self, request):
        tipo_venda = TipoVenda.objects.all()
        return render(request, self.template_name, {'tipo_venda': tipo_venda})

    def post(self, request):
        tipo_venda_id = request.POST.get('tipo_venda')
        try:
            tipo_venda_id = int(tipo_venda_id)
        except (ValueError, TypeError):
            return redirect('nova_venda')

        tipo_venda = get_object_or_404(TipoVenda, id=tipo_venda_id)

        if tipo_venda.tipo == 'Entrega':
            form = VendaEntregaForm(request.POST or None)
        elif tipo_venda.tipo == 'Retirada':
            form = VendaRetiradaForm(request.POST or None)
        elif tipo_venda.tipo == 'Local':
            form = VendaLocalForm(request.POST or None)

        if form.is_valid():
            dados = form.save(commit=False)
            dados.tipo_venda = tipo_venda  # Adiciona o tipo de venda
            dados.save()
            return redirect('adicionar_produtos', venda_id=nova_venda.identificador_unico)

        return render(request, self.template_name, {'form': form, 'tipo_venda': tipo_venda})
    
    
class AdicionarProdutosView(View):
    template_name = 'adicionar_produtos.html'

    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        produtos = Produto.objects.all()
        form = VendaDoProdutoForm(venda=venda)
        return render(request, self.template_name, {'venda': venda, 'produtos': produtos, 'form': form})

    def post(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        form = VendaDoProdutoForm(request.POST, venda=venda)
        
        if form.is_valid():
            item_venda = form.save(commit=False)
            item_venda.venda = venda
            item_venda.save()
            return redirect('adicionar_produtos', venda_id=venda_id)

        produtos = Produto.objects.all()
        return render(request, self.template_name, {'venda': venda, 'produtos': produtos, 'form': form})
class FinalizarVendaView(View):
    template_name = 'finalizar_venda.html'

    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        itens_venda = venda.itens.all()
        return render(request, self.template_name, {'venda': venda, 'itens_venda': itens_venda})

    def post(self, request, venda_id):
        venda = get_object_or_404(Venda, identificador_unico=venda_id)
        # Aqui você pode adicionar lógica para processar o pagamento ou finalizar a venda
        return redirect('index')  # Redireciona para a página inicial ou uma página de confirmação