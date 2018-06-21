from django.conf.urls import url, include

from rest_framework import routers

from .views import AlunoViewSet, ModuloViewSet

router = routers.DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'modulos', ModuloViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
