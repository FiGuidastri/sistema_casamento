from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Usuario(AbstractUser):
    '''
    Modelo de usuário customizado que estende o AbstractUser do Django.
    Adiciona um campo 'tipo_usuario' para diferenciar os papéis no sistema
    '''
    class TipoUsuario(models.TextChoices):
        CASAL = 'CASAL', 'Casal'
        CERIMONIALISTA = 'CERIMONIALISTA', 'Cerimonialista'
        FORNECEDOR = 'FORNECEDOR', 'Fornecedor'
        ADMIN = 'ADMIN', 'Admin'

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.CASAL
    )

class Casal(models.Model):
    '''
    Perfil para usuarios do tipo 'Casal'
    Armazena informaçoes específicas do casal
    '''
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    nome_noivo = models.CharField(max_length=100)
    nome_noiva = models.CharField(max_length=100)
    data_casamento = models.DateField()
    orcamento_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.nome_noivo} & {self.nome_noiva}'

class Cerimonialista(models.Model):
    '''
    Perfil para usuarios do tipo cerimonialista
    '''
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    # lista de casais que cerimonialista gerencia
    casais = models.ManyToManyField(Casal, related_name='cerimonialistas')
    
    def __str__(self):
        return self.nome_completo
    
class Fornecedor(models.Model):
    """
    Perfil para usuários do tipo 'Fornecedor'.
    """
    CATEGORIAS = [
        ('BUFFET', 'Buffet'),
        ('DECORACAO', 'Decoração'),
        ('FOTOGRAFIA', 'Fotografia'),
        ('MUSICA', 'Música'),
        ('ESPACO', 'Espaço'),
        ('CONVITES', 'Convites'),
        ('OUTRO', 'Outro'),
    ]
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    nome_empresa = models.CharField(max_length=255)
    categoria_servico = models.CharField(max_length=50, choices=CATEGORIAS)
    contato_email = models.EmailField()
    telefone = models.CharField(max_length=20)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_empresa
    
# === Modelos de gestao do casamento ===

class Orcamento(models.Model):
    '''
    Armazena as propostas de orcamento dos fornecedores para um casal
    '''
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        APROVADO = 'APROVADO', 'Aprovado'
        RECUSADO = 'RECUSADO', 'Recusado'

    casal = models.ForeignKey(Casal, on_delete=models.CASCADE, related_name='orcamentos')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='orcamentos')
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orçamento de {self.fornecedor} para {self.casal}"

class Pagamento(models.Model):
    '''
    registra os pagamentos (á vista ou parcelados) de um orcamento aprovado
    '''
    class FormaPagamento(models.TextChoices):
        A_VISTA = 'A_VISTA', 'À Vista'
        PARCELADO = 'PARCELADO', 'Parcelado'

    class StatusPagamento(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        PAGO = 'PAGO', 'Pago'
        ATRASADO = 'ATRASADO', 'Atrasado'

    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='pagamentos')
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=StatusPagamento.choices, default=StatusPagamento.PENDENTE)
    forma_pagamento = models.CharField(max_length=10, choices=FormaPagamento.choices)
    comprovante = models.FileField(upload_to='comprovantes/', blank=True, null=True)

    def __str__(self):
        return f"Pagamento de {self.valor_parcela} para {self.orcamento.fornecedor}"
    
class Tarefa(models.Model):
    """
    Lista de tarefas a serem cumpridas pelo casal ou cerimonialista.
    """
    class Prioridade(models.IntegerChoices):
        BAIXA = 1, 'Baixa'
        MEDIA = 2, 'Média'
        ALTA = 3, 'Alta'

    casal = models.ForeignKey(Casal, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    data_limite = models.DateField()
    concluida = models.BooleanField(default=False)
    prioridade = models.IntegerField(choices=Prioridade.choices, default=Prioridade.MEDIA)

    def __str__(self):
        return self.titulo
    
class Documento(models.Model):
    """
    Armazena documentos importantes, como cópias de RG, comprovantes, etc.
    """
    casal = models.ForeignKey(Casal, on_delete=models.CASCADE, related_name='documentos')
    titulo = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='documentos/')
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Contrato(models.Model):
    """
    Gerencia os contratos assinados com os fornecedores.
    """
    orcamento = models.OneToOneField(Orcamento, on_delete=models.CASCADE, related_name='contrato')
    arquivo_contrato = models.FileField(upload_to='contratos/')
    assinado = models.BooleanField(default=False)
    data_assinatura = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Contrato para {self.orcamento}"

# --- Modelos Adicionais ---

class Visita(models.Model):
    casal = models.ForeignKey(Casal, on_delete=models.CASCADE, related_name='visitas')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='visitas')
    data_hora = models.DateTimeField()
    local = models.CharField(max_length=255)
    anotacoes = models.TextField(blank=True, null=True)

class Avaliacao(models.Model):
    casal = models.ForeignKey(Casal, on_delete=models.CASCADE, related_name='avaliacoes')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # Nota de 1 a 5
    comentario = models.TextField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)

class Timeline(models.Model):
    casal = models.ForeignKey(Casal, on_delete=models.CASCADE, related_name='timeline')
    evento = models.CharField(max_length=255) # Ex: "Degustação do Buffet", "Prova do vestido"
    data_evento = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)