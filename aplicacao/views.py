from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from aplicacao.forms import *
from .models import Produto
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

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

@login_required(login_url="url_entrar") 
def criar_cliente(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        perfil_form = PerfilClienteForm(request.POST)
        if cliente_form.is_valid() and perfil_form.is_valid():
            cliente = cliente_form.save(commit=False)
            perfil = perfil_form.save()
            cliente.perfil = perfil
            cliente.save()
            return redirect('url_clientes')  
    else:
        cliente_form = ClienteForm()
        perfil_form = PerfilClienteForm()

    return render(request, 'cadastrarCliente.html', {
        'cliente_form': cliente_form,
        'perfil_form': perfil_form,
    })

@login_required(login_url="url_entrar")
def criar_venda(request):
    prefix = 'items'
    venda_obj_temp = Venda()  

    if request.method == 'POST':
        venda_form = VendasForm(request.POST)

        # Remover
        if 'remove_item' in request.POST:
            idx = int(request.POST['remove_item'])
            post = request.POST.copy()
            delete_key = f'{prefix}-{idx}-DELETE'
            post[delete_key] = 'on'  
            formset = ItemVendaFormSet(post, instance=venda_obj_temp, prefix=prefix)
            return render(request, 'cadastrarVenda.html', {
                'venda_form': venda_form,
                'formset': formset,
            })

        # Adicionar
        if 'add_item' in request.POST:
            post = request.POST.copy()
            total_key = f'{prefix}-TOTAL_FORMS'
            total = int(post.get(total_key, 0))
            post[total_key] = str(total + 1)
            formset = ItemVendaFormSet(post, instance=venda_obj_temp, prefix=prefix)
            return render(request, 'cadastrarVenda.html', {
                'venda_form': venda_form,
                'formset': formset,
            })

        # Salvar
        if venda_form.is_valid():
            venda_obj = venda_form.save(commit=False)
            formset = ItemVendaFormSet(request.POST, instance=venda_obj, prefix=prefix)
            if formset.is_valid():
                with transaction.atomic():
                    venda_obj.save()
                    formset.save()
                return redirect('url_vendas')
        else:
            formset = ItemVendaFormSet(request.POST, instance=venda_obj_temp, prefix=prefix)

    else:
        # GET inicial
        venda_form = VendasForm()
        formset = ItemVendaFormSet(instance=venda_obj_temp, prefix=prefix)

    return render(request, 'cadastrarVenda.html', {
        'venda_form': venda_form,
        'formset': formset,
    })

@login_required(login_url="url_entrar")
def editar_venda(request, pk):
    prefix = 'items'                  
    venda = get_object_or_404(Venda, pk=pk)

    if request.method == 'POST':
        venda_form = VendasForm(request.POST, instance=venda)

        formset = ItemVendaFormSet(request.POST, instance=venda, prefix=prefix)

        # Remover
        if 'remove_item' in request.POST:
            idx = int(request.POST['remove_item'])
            post = request.POST.copy()                 
            delete_key = f'{prefix}-{idx}-DELETE'    
            post[delete_key] = 'on'                  
            formset = ItemVendaFormSet(post, instance=venda, prefix=prefix)
            return render(request, 'editarVenda.html', {
                'venda_form': venda_form,
                'formset': formset,
                'venda': venda,                         
            })

        # Adicionar
        if 'add_item' in request.POST:
            post = request.POST.copy()
            total_key = f'{prefix}-TOTAL_FORMS'       
            total = int(post.get(total_key, 0))
            post[total_key] = str(total + 1)     
            formset = ItemVendaFormSet(post, instance=venda, prefix=prefix)
            return render(request, 'editarVenda.html', {
                'venda_form': venda_form,
                'formset': formset,
                'venda': venda,
            })

        # Salvar
        if venda_form.is_valid():
            
            venda_form.save(commit=False)

            formset = ItemVendaFormSet(request.POST, instance=venda, prefix=prefix)

            if formset.is_valid():
                with transaction.atomic():
                    venda_form.save()
                    formset.save()

            # Dá para simplficar tudo isso aqui com o código acima --> faltava mandar o id pelo DOM
            '''for item in formset:
                if item.is_valid():
                    item.save()
            
            for key, value in request.POST.items():
                if key.startswith( prefix + "-") and key.endswith("-DELETE") and value == "on":
                    idx = key.split("-")[1]
                    item_id_key = f"{prefix}-{idx}-id"
                    item_id = request.POST.get(item_id_key)
                    if item_id:
                        ItemVenda.objects.filter(id=item_id).delete()
               ''' 

            return redirect('url_vendas')
        else:
            formset = ItemVendaFormSet(request.POST, instance=venda, prefix=prefix)

        return render(request, 'editarVenda.html', {
            'venda_form': venda_form,
            'formset': formset,
            'venda': venda,
        })

    else:
        venda_form = VendasForm(instance=venda)
        formset = ItemVendaFormSet(instance=venda, prefix=prefix)
        return render(request, 'editarVenda.html', {
            'venda_form': venda_form,
            'formset': formset,
            'venda': venda,
        })

@login_required(login_url="url_entrar")
def deletarVenda ( request, id ):

    venda = get_object_or_404(Venda, id=id)

    if request.method == "GET":

        context = {
            'venda': venda
        }

        return render(request, 'deletarVenda.html', context)

    elif request.method == "POST":

        venda.delete()


    return redirect("url_vendas")

@login_required(login_url="url_entrar")
def vendas ( request ):
    vendas = Venda.objects.all()
    context = {
        'vendas': vendas,
    }
    return render( request, 'vendas.html', context)

@login_required(login_url="url_entrar")
def clientes ( request ):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
    }
    return render( request, 'clientes.html', context)

@login_required(login_url="url_entrar")
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        perfilForm = PerfilClienteForm(request.POST, instance=cliente.perfil)
        if form.is_valid() and perfilForm.is_valid():
            form.save()
            perfilForm.save()
            return redirect("url_clientes")
    else:
        form = ClienteForm(instance=cliente)
        perfilForm = PerfilClienteForm(instance=cliente.perfil)

    return render(request, 'editarCliente.html', {'cliente_form': form, 'perfil_form': perfilForm})

@login_required(login_url="url_entrar")
def deletarCliente ( request, id ):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "GET":

        context = {
            'cliente': cliente
        }

        return render(request, 'deletarCliente.html', context)

    elif request.method == "POST":

        cliente.delete()


    return redirect("url_clientes")

def sair(request):
    logout(request)
    return redirect('url_entrar')

def custom_404(request):
    return render(request, '404.html', status=404)