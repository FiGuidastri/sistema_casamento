# casamento/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Casal, Cerimonialista, Fornecedor,
    Orcamento, Pagamento, Tarefa, Documento, Contrato,
    Visita, Avaliacao, Timeline
)

# --- Customizações do Admin ---

class CasalInline(admin.StackedInline):
    model = Casal
    can_delete = False
    verbose_name_plural = 'Perfil Casal'

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    inlines = (CasalInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'groups')
    
    # Adiciona o nosso campo customizado 'tipo_usuario' ao formulário de edição do usuário.
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome_empresa', 'categoria_servico', 'contato_email', 'telefone')
    list_filter = ('categoria_servico',)
    search_fields = ('nome_empresa', 'contato_email')

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'casal', 'data_limite', 'prioridade', 'concluida')
    list_filter = ('concluida', 'prioridade', 'data_limite')
    search_fields = ('titulo', 'casal__nome_noivo', 'casal__nome_noiva')

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'valor', 'status', 'data_criacao')
    list_filter = ('status', 'fornecedor__categoria_servico')
    search_fields = ('casal__nome_noivo', 'fornecedor__nome_empresa')

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('orcamento', 'valor_parcela', 'data_vencimento', 'status')
    list_filter = ('status', 'forma_pagamento', 'data_vencimento')
    search_fields = ('orcamento__casal__nome_noivo', 'orcamento__fornecedor__nome_empresa')

# Registramos os outros modelos que não precisam de customização complexa
admin.site.register(Cerimonialista)
admin.site.register(Documento)
admin.site.register(Contrato)
admin.site.register(Visita)
admin.site.register(Avaliacao)
admin.site.register(Timeline)
# O modelo Casal não é registrado aqui pois ele é editado 'inline' dentro do Usuário.