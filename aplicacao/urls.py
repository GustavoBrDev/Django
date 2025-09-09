from django.urls import path
from . import views

urlpatterns = [
    
    # Produtos
    path('produtos', views.produtos, name="url_produtos"),
    path('cadastrar-produto', views.cadastrarProduto, name="url_cadastrar_produto"),
    path('atualizar-produto/<int:id>', views.atualizarProduto, name="url_editar_produto"),
    path('deletar-produto/<int:id>', views.deletarProduto, name="url_deletar_produto"),
    
    # Vendas
    path('vendas', views.vendas, name="url_vendas"),
    path('vendas/novo/', views.criar_venda, name='criar_venda'),
    path('vendas/<int:pk>/editar/', views.editar_venda, name='editar_venda'),
    path('deletar-venda/<int:id>', views.deletarVenda, name='deletar_venda'),

    # Clientes
    path('clientes', views.clientes, name='url_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('deletar-cliente/<int:id>', views.deletarCliente, name='deletar_cliente'),

    # Autenticação
    path('entrar', views.entrar, name="url_entrar"),
    path('cad_user', views.cad_user, name="url_cad_user"),
    path('sair', views.sair, name="url_sair"),

    # Outros
    path('', views.index, name="url_index"),
    path('404-preview/', views.custom_404, name='404_preview'),
]
