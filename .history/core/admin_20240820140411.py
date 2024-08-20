from django.contrib import admin
from .models import *

admin.site.register(TipoVenda)
admin.site.register(Entregador)
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Atendente)
admin.site.register(Venda)
admin.site.register(VendaEntrega)
admin.site.register(VendaRetirada)
admin.site.register(VendaLocal)
admin.site.register(ItemVenda)
