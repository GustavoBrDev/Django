from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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

def cadastrarProduto ( request ):

    if request.method == "GET":
        return render( request, 'novoProduto.html')
    elif request.method == "POST":

        nome = request.POST.get("nome")
        
        try:
            preco = float(request.POST.get("preco").replace(',', '.'))
        except:
            preco = 0

        try:
            qtde = request.POST.get("qtde")
        except:
            qtde = 0

        produto = Produto (
            nome = nome,
            preco = preco,
            qtde = qtde
        )

        Produto.save(produto)

        return redirect("url_produtos")

def atualizarProduto (request, id ):

    produto = get_object_or_404(Produto, id=id)

    if request.method == "GET":
        context = {
            'produto': produto
        }

        return render(request, 'editarProduto.html', context)

    elif request.method == "POST":

        nome = request.POST.get("nome")
        
        try:
            preco = float(request.POST.get("preco").replace(',', '.'))
        except:
            preco = 0

        try:
            qtde = request.POST.get("qtde")
        except:
            qtde = 0

        produto.nome = nome
        produto.qtde = qtde
        produto.preco = preco
        produto.save()
        return redirect("url_produtos")

def deletarProduto ( request, id ):

    produto = get_object_or_404(Produto, id=id)

    if request.method == "GET":

        context = {
            'produto': produto
        }

        return render(request, 'deletarProduto.html', context)

    elif request.method == "POST":

        produto.delete()


    return redirect("url_produtos")

def custom_404(request):
    return render(request, '404.html', status=404)