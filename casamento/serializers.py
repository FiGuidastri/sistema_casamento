from rest_framework import serializers
from .models import (
    Usuario, Casal, Cerimonialista, Fornecedor,
    Orcamento, Pagamento, Tarefa, Documento, Contrato,
    Visita, Avaliacao, Timeline
)

# Usamos ModelSerializer que cria os campos e validações automaticamente a partir do modelo.

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Campos que serão expostos na API. A senha não é exposta para leitura.
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'password']
        extra_kwargs = {
            'password': {'write_only': True} # 'write_only' significa que o campo é usado para criar/atualizar, mas não é retornado em leituras.
        }

    def create(self, validated_data):
        # Sobrescrevemos o método create para garantir que a senha seja salva corretamente (com hash).
        user = Usuario.objects.create_user(**validated_data)
        return user

class CasalSerializer(serializers.ModelSerializer):
    # Para LEITURA: continua mostrando o nome de usuário para fácil identificação
    username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Casal
        # O campo 'usuario' será usado para ESCRITA (receberá o ID do usuário)
        # O campo 'username' será usado para LEITURA (exibirá o nome)
        fields = ['usuario', 'nome_noivo', 'nome_noiva', 'data_casamento', 'orcamento_total', 'username']
        extra_kwargs = {
            # Oculta o campo 'usuario' (que espera um ID) da resposta da API,
            # mostrando apenas os detalhes mais amigáveis.
            'usuario': {'write_only': True}
        }

    class Meta:
        model = Casal
        fields = '__all__' # Inclui todos os campos do modelo

class FornecedorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Fornecedor
        fields = '__all__'

class CerimonialistaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Cerimonialista
        fields = '__all__'

# --- Serializers para Gestão do Casamento ---

class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = '__all__'

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'