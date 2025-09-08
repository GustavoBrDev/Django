from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():

            if isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            else:
                css_class = "form-input"
            
            field.widget.attrs.update({'class': css_class})
            field.widget.attrs.setdefault('placeholder', field.label)

class PerfilClienteForm ( BaseStyledForm ):
    class Meta:
        model=PerfilCliente
        fields=["endereco", "telefone"]

class ClienteForm ( ModelForm ):
    class Meta:
        model=Cliente
        fields=["nome", "email"]


class VendasForm(BaseStyledForm):
    class Meta:
        model = Venda
        fields = ['cliente']

class ItemVendaForm(BaseStyledForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

ItemVendaFormSet = inlineformset_factory(
    Venda,
    ItemVenda,
    fields=('produto','quantidade'),
    extra=1,
    can_delete=True
)