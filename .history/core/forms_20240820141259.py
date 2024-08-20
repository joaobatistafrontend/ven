
from django import forms
from .models import*

class VendaEntregaForm(forms.ModelForm):
    class Meta:
        model = VendaEntrega
        fields = ['entregador']

class VendaRetiradaForm(forms.ModelForm):
    class Meta:
        model = DadosRetirada
        fields = []

class VendaLocalForm(forms.ModelForm):
    class Meta:
        model = DadosVendaLocal
        fields = ['atendente', 'mesa']