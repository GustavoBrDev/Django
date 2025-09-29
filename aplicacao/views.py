from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from aplicacao.forms import *
from .models import Produto
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import io
import urllib, base64
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Aqui são feitas as views

# Funções auxiliares

def get_dataframe():
    # Busca todos os dados do banco e retorna um DataFrame do Pandas
    avaliacoes = Avaliacao.objects.all().values()
    df = pd.DataFrame(list(avaliacoes))
    df = df.dropna()
    return df
def plot_to_base64(fig):
    # Converte uma figura Matplotlib para uma string base64 para ser usada no HTML
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)


# Produtos
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

# Vendas
@login_required(login_url="url_entrar")
def vendas ( request ):
    vendas = Venda.objects.all()
    context = {
        'vendas': vendas,
    }
    return render( request, 'vendas.html', context)

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

# Clientes
@login_required(login_url="url_entrar")
def clientes ( request ):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
    }
    return render( request, 'clientes.html', context)

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

# Autenticação 
def sair(request):
    logout(request)
    return redirect('url_entrar')
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

# Dashboard


@login_required(login_url="url_entrar")
def dashboard ( request, show ): #View --> Responsável por chamar e 'renderizar' os gráficos
    
    graficos = {}

    if any(w in show.lower() for w in ["user","users","activeuser","activeusers"]):
        graficos['grafico_usuarios_ativos'] = usuarios_mais_ativos()
    
    if any(w in show.lower() for w in ["review","evolution","reviews"]):
        graficos['grafico_evolucao_reviews'] = evolucao_reviews()
    
    if any(w in show.lower() for w in ["price","prices","score", "scores"]):
        graficos['grafico_preco_score'] = preco_vs_score()
    
    if any(w in show.lower() for w in ["bad","good","emotions", "feeling"]):
        graficos['grafico_sentimento'] = sentimento_reviews()

    if any(w in show.lower() for w in ["book","top","books", "best", "most"]):
        graficos['grafico_top_livros'] = livros_mais_avaliados()
    
    if any(w in show.lower() for w in ["grade","grade","note", "notes"]):
        graficos['grafico_distribuicao_notas'] = distribuicao_das_notas()
    
    return render(request, 'dashboard.html', graficos)

def usuarios_mais_ativos ():

    # Tratamento de Dados
    df = get_dataframe()
    df = df.copy()

    df['profile_name'] = df['profile_name'].where(pd.notnull(df['profile_name']), None)
    df['profile_name'] = df['profile_name'].astype(str).str.strip()

    invalid_literals = {'', 'nan', 'none', 'null', 'desconhecido', 'n/d', 'na'}
    mask_invalid = df['profile_name'].str.lower().isin(invalid_literals)

    df.loc[mask_invalid, 'profile_name'] = np.nan
    df = df.dropna(subset=['profile_name'])

    df['primeiro_nome'] = df['profile_name'].str.split().str[:2].str.join(" ")

    df.loc[df['primeiro_nome'].str.strip() == '', 'primeiro_nome'] = np.nan
    df = df.dropna(subset=['primeiro_nome'])
    df = df[df['primeiro_nome'].str.len() >= 3]

    usuarios_ativos = df['primeiro_nome'].value_counts().nlargest(15).sort_values()

    # Gera o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    cores = ['#72BCA5', '#F4DDB4', '#F1AE2B', '#BC0B27', '#4A2512']  
    usuarios_ativos.plot(kind='barh', ax=ax, color=cores)
    ax.set_title("Top 15 Usuários Mais Ativos")
    ax.set_xlabel("Número de Avaliações")
    ax.set_ylabel("Usuário")
    plt.tight_layout()

    grafico_usuarios_ativos = plot_to_base64(fig)
    plt.close(fig)
    return grafico_usuarios_ativos

def evolucao_reviews():

    # Tratamento de Dados
    df = get_dataframe()
    df = df.copy()

    df = df.dropna(subset=['review_time'])
    df['data_review'] = pd.to_datetime(df['review_time'], unit='s', errors='coerce')
    df = df.dropna(subset=['data_review'])

    df['ano'] = df['data_review'].dt.year
    avaliacoes_por_ano = df.groupby('ano').size().sort_index()

    # Gera o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(avaliacoes_por_ano.index, avaliacoes_por_ano.values, marker='o', linestyle='-', color='teal')
    ax.set_title("Evolução do Número de Avaliações por Ano")
    ax.set_xticks(avaliacoes_por_ano.index)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Quantidade de Avaliações")
    ax.grid(True)
    fig.tight_layout()

    grafico_evolucao_reviews = plot_to_base64(fig)
    plt.close(fig)
    return grafico_evolucao_reviews

def preco_vs_score ():

    # Tratamento de Dados
    df = get_dataframe()
    df = df.copy()

    df = df[df['price'] > 0]
    df = df[df['price'] < 100]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['price'], df['review_score'], alpha=0.3, color='darkblue')

    ax.set_title("Correlação entre Preço e Nota da Avaliação")
    ax.set_xlabel("Preço (R$)")
    ax.set_ylabel("Nota da Avaliação")
    ax.grid(True)

    fig.tight_layout()

    grafico_preco_reviews = plot_to_base64(fig)
    plt.close(fig)
    return grafico_preco_reviews

def sentimento_reviews ():

    # Tratamento de Dados
    df = get_dataframe()
    df = df.copy()

    df['review_summary'] = df['review_summary'].fillna('').str.lower()
    df['sentimento'] = df['review_summary'].apply(analisarTexto)
    contagem = df['sentimento'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        contagem.values,
        labels=contagem.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['lightgreen', 'salmon', 'lightgray']
    )

    ax.set_title('Distribuição de Sentimentos nos Sumários das Avaliações')
    ax.axis('equal')
    fig.tight_layout()

    grafico_sentimento = plot_to_base64(fig)
    plt.close(fig)
    return grafico_sentimento



def analisarTexto ( texto ):
    positivas = ['good', 'great', 'excellent', 'i loved', 'i recommend', "the best of all"]
    negativas = ['bad', 'terrible', 'disappointing', "i didn't like it", "horrible", "fuck", "shit"]

    texto = texto.lower()
    if any(p in texto for p in positivas):
        return 'Positivo'
    elif any(n in texto for n in negativas):
        return 'Negativo'
    else:
        return 'Neutro'


def distribuicao_das_notas():

    # Tratamento de Dados
    df = get_dataframe()
    df = df.copy()

    plt.figure(figsize=(10, 6))
    df['review_score'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Distribuição das Notas das Avaliações')
    plt.xlabel('Nota (Score)')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    grafico_distribuicao_notas = plot_to_base64(plt.gcf())
    plt.close()
    return grafico_distribuicao_notas

def livros_mais_avaliados():

    # Tratamento de Dados
    df = get_dataframe()
    df = df.copy()

    top_10_livros = df['title'].value_counts().nlargest(10)
    plt.figure(figsize=(12, 8))
    top_10_livros.sort_values().plot(kind='barh', color='coral')
    plt.title('Top 10 Livros com Mais Avaliações')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Título do Livro')
    plt.tight_layout()
    grafico_top_livros = plot_to_base64(plt.gcf())
    plt.close()
    return grafico_top_livros

# Outros

def index ( request ):
    context = {
        "texto": "Olá mundo!",
    }
    return render( request, 'index.html', context)

def custom_404(request):
    return render(request, '404.html', status=404)