from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="url_index"),
    path('produtos', views.produtos, name="url_produtos"),
    path('cadastrar-produto', views.cadastrarProduto, name="url_cadastrar_produto"),
    path('atualizar-produto/<int:id>', views.atualizarProduto, name="url_editar_produto"),
    path('deletar-produto/<int:id>', views.deletarProduto, name="url_deletar_produto"),
    path('entrar', views.entrar, name="url_entrar"),
    path('cad_user', views.cad_user, name="url_cad_user"),
    path('sair', views.sair, name="url_sair"),
    path('404-preview/', views.custom_404, name='404_preview'),
]
