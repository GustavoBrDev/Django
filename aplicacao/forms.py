from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

class PerfilClienteForm ( ModelForm ):
    class Meta:
        model=PerfilCliente
        fields=["endereco", "telefone"]

class ClienteForm ( ModelForm ):
    class Meta:
        model=Cliente
        fields=["nome", "email"]

class VendasForm ( ModelForm ):
    class Meta:
        model=Vendas
        fields=["cliente", "data"]

ItemVendaFormSet = inlineformset_factory(
    Vendas,
    ItemVenda,
    fields=('produto','quantidade'),
    extra=1,
    can_delete=True
)