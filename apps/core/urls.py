from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views

from .views import AlunoViewSet, ModuloViewSet, PerfilPerguntaViewSet, \
    GrupoViewSet, PlacarViewSet, QuestaoViewSet, PerguntaFlowViewSet, \
    DesafioViewSet

router = routers.DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'modulos', ModuloViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'placar', PlacarViewSet)
router.register(r'questoes', QuestaoViewSet)
router.register(r'perguntas_perfil', PerfilPerguntaViewSet, 'perguntas-perfil')
router.register(r'perguntas_flow', PerguntaFlowViewSet)
router.register(r'desafio', DesafioViewSet)


urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls'))
]
