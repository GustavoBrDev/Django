from django.db import models
from phone_field import PhoneField

class Produto ( models.Model ):
    nome = models.CharField("Nome", max_length=200, null=True)
    preco = models.DecimalField("Preco", decimal_places=2, max_digits=8, null=True)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null=True)

    def __str__(self):
        return self.nome

class PerfilCliente ( models.Model ):
    endereco = models.CharField("Endereco", max_length=100, null=False)
    telefone = PhoneField("Telefone", max_length=50)   

    def __str__(self):
        return self.endereco + self.telefone

class Cliente ( models.Model ):
    nome = models.CharField("Nome", max_length=200, null=True)
    email = models.EmailField("Email", max_length=100, null=False, unique=True)
    perfil = models.OneToOneField( PerfilCliente, null=False, on_delete=models.CASCADE, related_name="perfil")

    def __str__(self):
        return self.nome
    
class Venda ( models.Model ):
    cliente = models.ForeignKey( Cliente, null=False, on_delete=models.CASCADE)
    data = models.DateTimeField ( "Data", auto_now_add=True, null=False)
    produtos = models.ManyToManyField("Produto", through="ItemVenda")

class ItemVenda ( models.Model ):
    venda = models.ForeignKey("Venda", null=False, on_delete=models.CASCADE)
    produto = models.ForeignKey("Produto", null=False, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField("Quantidade", default=0)

class Avaliacao(models.Model):
    id_evaluation = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    profile_name = models.CharField(max_length=255, null=True, blank=True)
    review_helpfulness = models.CharField(max_length=20, null=True, blank=True)
    review_score= models.FloatField()
    review_time = models.IntegerField()
    review_summary = models.CharField(max_length=255, null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
   
    def __str__(self):
        return f"{self.title} - Score: {self.review_score}"

