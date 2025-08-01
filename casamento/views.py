# casamento/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated # Importamos a permissão

from .models import (
    Usuario, Casal, Cerimonialista, Fornecedor,
    Orcamento, Pagamento, Tarefa, Documento, Contrato,
    Visita, Avaliacao, Timeline
)
from .serializers import (
    UsuarioSerializer, CasalSerializer, CerimonialistaSerializer, FornecedorSerializer,
    OrcamentoSerializer, PagamentoSerializer, TarefaSerializer, DocumentoSerializer,
    ContratoSerializer, VisitaSerializer, AvaliacaoSerializer, TimelineSerializer
)

# Um ViewSet define a lógica para um conjunto de views relacionadas.
# ModelViewSet fornece implementações padrão para list, create, retrieve, update, e destroy.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    # 2. Adicione este método para controlar as permissões por ação
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que esta view requer.
        """
        if self.action == 'create':
            # Se a ação for 'create', permite o acesso para qualquer um.
            self.permission_classes = [AllowAny,]
        # Para todas as outras ações (list, retrieve, update, etc.), usa o padrão (IsAuthenticated).
        return super(self.__class__, self).get_permissions()

class CasalViewSet(viewsets.ModelViewSet):
    queryset = Casal.objects.all()
    serializer_class = CasalSerializer
    permission_classes = [IsAuthenticated] # Protege o endpoint. Só usuários autenticados podem acessar.

class CerimonialistaViewSet(viewsets.ModelViewSet):
    queryset = Cerimonialista.objects.all()
    serializer_class = CerimonialistaSerializer
    permission_classes = [IsAuthenticated]

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]

class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    permission_classes = [IsAuthenticated]

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuthenticated]

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]

class TimelineViewSet(viewsets.ModelViewSet):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = [IsAuthenticated]