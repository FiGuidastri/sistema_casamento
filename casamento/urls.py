# casamento/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, CasalViewSet, CerimonialistaViewSet, FornecedorViewSet,
    OrcamentoViewSet, PagamentoViewSet, TarefaViewSet, DocumentoViewSet,
    ContratoViewSet, VisitaViewSet, AvaliacaoViewSet, TimelineViewSet
)

# O DefaultRouter registra automaticamente as URLs para um ViewSet.
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'casais', CasalViewSet)
router.register(r'cerimonialistas', CerimonialistaViewSet)
router.register(r'fornecedores', FornecedorViewSet)
router.register(r'orcamentos', OrcamentoViewSet)
router.register(r'pagamentos', PagamentoViewSet)
router.register(r'tarefas', TarefaViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'contratos', ContratoViewSet)
router.register(r'visitas', VisitaViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'timeline', TimelineViewSet)

# As URLs da API são agora determinadas automaticamente pelo roteador.
urlpatterns = [
    path('', include(router.urls)),
]