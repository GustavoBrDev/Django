from django.shortcuts import render

# Aqui são feitas as views
def index ( request ):
    context = {
        "texto": "Olá mundo!",
    }
    return render( request, 'index.html', context)

def produtos ( request ):
    return render( request, 'produtos.html')