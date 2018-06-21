from django.conf.urls import url, include

from rest_framework import routers

from .views import AlunoViewSet, ModuloViewSet, PerfilPerguntaViewSet, \
    GrupoViewSet, PlacarViewSet, QuestaoViewSet

router = routers.DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'modulos', ModuloViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'placar', PlacarViewSet)
router.register(r'questoes', QuestaoViewSet)
router.register(r'perguntas_perfil', PerfilPerguntaViewSet)


urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
