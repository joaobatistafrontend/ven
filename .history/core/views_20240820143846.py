from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from django.shortcuts import render

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

        print(f"Tipo Venda ID: {tipo_venda_id}")  # Debugging
        
        tipo_venda = get_object_or_404(TipoVenda, id=tipo_venda_id)
        
        # Criação de uma nova venda associada ao tipo de venda selecionado
        nova_venda = Venda.objects.create(tipo_venda=tipo_venda)

        # Redireciona para a página de adição de produtos com base no tipo de venda
        if tipo_venda.tipo == 'Entrega':
            form = VendaEntregaForm()
        elif tipo_venda.tipo == 'Retirada':
            form = VendaRetiradaForm()
        elif tipo_venda.tipo == 'Local':
            form = VendaLocalForm()

        # Depois de selecionar o tipo de venda, redirecionar para a adição de produtos
        return render(request, 'adicionar_produtos.html', {'form': form, 'venda': nova_venda})

class AdicionarProdutosView(View):
    template_name = 'adicionar_produtos.html'

    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, id=venda_id)
        produtos = Produto.objects.all()
        return render(request, self.template_name, {'venda': venda, 'produtos': produtos})

    def post(self, request, venda_id):
        venda = get_object_or_404(Venda, id=venda_id)
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade'))

        produto = get_object_or_404(Produto, id=produto_id)
        
        # Crie ou atualize o item de venda
        item_venda, created = VendaDoProduto.objects.get_or_create(
            venda=venda,
            produto=produto,
            defaults={'qtd': quantidade, 'total': produto.valor * quantidade}
        )
        
        if not created:
            # Se o item já existir, apenas atualize a quantidade e o total
            item_venda.qtd += quantidade
            item_venda.total = item_venda.qtd * produto.valor
            item_venda.save()

        return redirect('adicionar_produtos', venda_id=venda.id)
class FinalizarVenda(View):
    template_name = 'finalizar_venda.html'

    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, id=venda_id)
        itens_venda = VendaDoProduto.objects.filter(venda=venda)
        return render(request, self.template_name, {'venda': venda, 'itens_venda': itens_venda})

    def post(self, request, venda_id):
        # Finalizar a venda e confirmar o pagamento
        venda = get_object_or_404(Venda, id=venda_id)
        venda.finalizada = True  # Definir um status, se necessário
        venda.save()
        
        return redirect('index')