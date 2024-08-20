
from django import forms
from .models import*

class VendaEntregaForm(forms.ModelForm):
    class Meta:
        model = DadosEntrega
        fields = ['entregador', 'bairroPadrao', 'nome_cliente', 'telefone_cliente', 'endereco', 'pontoReferencia']


class VendaRetiradaForm(forms.ModelForm):
    class Meta:
        model = DadosRetirada
        fields = ['nome_cliente','telefone_cliente']

class VendaLocalForm(forms.ModelForm):
    class Meta:
        model = DadosVendaLocal
        fields = ['vendedor', 'numero_mesa']

class VendaDoProdutoForm(forms.ModelForm):
    class Meta:
        model = VendaDoProduto
        fields = ['produto', 'qtd']

    def __init__(self, *args, **kwargs):
        self.venda = kwargs.pop('venda', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        qtd = cleaned_data.get('qtd')

        if produto and qtd:
            # Calcula o total baseado no valor do produto e na quantidade
            total = produto.valor * qtd
            cleaned_data['total'] = total

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
