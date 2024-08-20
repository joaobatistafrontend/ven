
from django import forms
from .models import*

class VendaEntregaForm(forms.ModelForm):
    class Meta:
        model = DadosEntrega
        fields = ['entregador','bairroPadrao','nome_cliente','telefone_cliente','endereco','pontoReferencia']

class VendaRetiradaForm(forms.ModelForm):
    class Meta:
        model = DadosRetirada
        fields = ['nome_cliente','telefone_cliente']

class VendaLocalForm(forms.ModelForm):
    class Meta:
        model = DadosVendaLocal
        fields = ['vendedor', 'numero_mesa']