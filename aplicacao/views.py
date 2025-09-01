from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Produto
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Aqui são feitas as views
def index ( request ):
    context = {
        "texto": "Olá mundo!",
    }
    return render( request, 'index.html', context)

@login_required(login_url="url_entrar")
def produtos ( request ):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render( request, 'produtos.html', context)

@login_required(login_url="url_entrar")
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

@login_required(login_url="url_entrar")
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

@login_required(login_url="url_entrar")
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

def entrar(request):
    if request.method == "GET":
        return render(request, "entrar.html")
    else:
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('url_produtos')
        else:
            return HttpResponse("Falha no login")

def cad_user(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        user = User.objects.filter(username=nome).first()

        if user:
            return HttpResponse("Usuário já existe")

        user = User.objects.create_user(username=nome, email=email, password=senha)

        user.save()
        messages.success(request, "Usuário cadastrado")
        return render(request, "cad_user.html")
    else:
        return render(request, "cad_user.html")
    
def sair(request):
    logout(request)
    return redirect('url_entrar')

def custom_404(request):
    return render(request, '404.html', status=404)