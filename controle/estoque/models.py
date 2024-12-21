from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    vencimento = models.DateField()

    def __str__(self):
        return self.nome

   
class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('funcionario', 'Funcionário'),
        ('admin', 'Administrador'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo_user = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return self.nome

    

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

 

class MovimentoEstoque(models.Model):
    TIPO_MOVIMENTO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTO)
    data_movimento = models.DateField(auto_now_add=True)
    responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.produto.nome

    
