from django.shortcuts import render
from .models import Produto

# Aqui são feitas as views
def index ( request ):
    context = {
        "texto": "Olá mundo!",
    }
    return render( request, 'index.html', context)

def produtos ( request ):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render( request, 'produtos.html', context)

def custom_404(request):
    return render(request, '404.html', status=404)