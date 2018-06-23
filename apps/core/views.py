from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Aluno, Modulo, PerfilPergunta, Grupo, Placar, Questao
from .serializers import AlunoSerializer, ModuloSerializer, \
    PerfilPerguntaSerializer, GrupoSerializer, PlacarSerializer, QuestaoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.filter(ativo=True)
    serializer_class = ModuloSerializer

    @action(methods=['get'], detail=False)
    def ativo(self, request):
        modulo = Modulo.objects.get(ativo=True)
        serializer = self.get_serializer(modulo)
        return Response(serializer.data)


class PerfilPerguntaViewSet(viewsets.ModelViewSet):
    queryset = PerfilPergunta.objects.all()
    serializer_class = PerfilPerguntaSerializer


class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.filter(modulo__ativo = True)
    serializer_class = GrupoSerializer


class PlacarViewSet(viewsets.ModelViewSet):
    queryset = Placar.objects.filter(grupo__modulo__ativo = True).order_by('pontos')
    serializer_class = PlacarSerializer


class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.get(ativo=True).questao_set.all()
    serializer_class = QuestaoSerializer
    
