from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date

class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.nome}'



class TipoVenda(models.Model):  # Renomeado para seguir convenção de nomenclatura
    tipo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.tipo

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Certifique-se de que esse campo existe

    tipo_categoria = models.ForeignKey(NovaCategoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome_produto} - {self.tipo_categoria.nome} - R${self.valor}"

class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.produto.nome_produto} - {self.qtd} unidades"

class Venda(models.Model):
    # Campos do modelo
    tipo_venda = models.ForeignKey(TipoVenda, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)
    identificador_unico = models.AutoField(primary_key=True)  # Ou utilize 'id' se for o padrão

    def __str__(self):
        return str(self.identificador_unico)
    
    

class VendaDoProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.produto.nome_produto} - {self.qtd} unidades - Total: R${self.total}"

@receiver(pre_save, sender=VendaDoProduto)
def update_total(sender, instance, **kwargs):
    if instance.produto.valor and instance.qtd:
        instance.total = instance.produto.valor.valor * instance.qtd
    else:
        instance.total = 0

class EntregaBairro(models.Model):
    bairro = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.bairro} - R${self.valor}'

class Entregador(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.IntegerField(blank=True, null=True)
    veiculo = models.CharField(max_length=100, null=True, blank=True)
    placa = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.veiculo} {self.placa}"

class Atendente(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

class DadosEntrega(models.Model):
    venda = models.OneToOneField(Venda, on_delete=models.CASCADE)  # Associado a uma venda
    entregador = models.ForeignKey(Entregador, on_delete=models.CASCADE)
    bairroPadrao = models.ForeignKey(EntregaBairro, on_delete=models.CASCADE)
    nome_cliente = models.CharField(max_length=100, blank=True, null=True)
    telefone_cliente = models.IntegerField(blank=True, null=True)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    pontoReferencia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.entregador} - {self.bairroPadrao} - {self.nome_cliente}"

class DadosRetirada(models.Model):
    venda = models.OneToOneField(Venda, on_delete=models.CASCADE)  # Associado a uma venda
    nome_cliente = models.CharField(max_length=100, blank=True, null=True)
    telefone_cliente = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_cliente} - {self.telefone_cliente}"

class DadosVendaLocal(models.Model):
    venda = models.OneToOneField(Venda, on_delete=models.CASCADE)  # Associado a uma venda
    vendedor = models.ForeignKey(Atendente, on_delete=models.CASCADE)
    numero_mesa = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.vendedor} - Mesa {self.numero_mesa}"
