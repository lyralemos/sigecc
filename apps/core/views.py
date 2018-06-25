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
        try:
            modulo = Modulo.objects.get(ativo=True)
            serializer = self.get_serializer(modulo)
            return Response(serializer.data)
        except Modulo.DoesNotExist:
            return Response({})

    def chunks(self, l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i+n]

    @action(methods=['get'], detail=False)
    def liberar(self, request):
        modulo = Modulo.objects.get(ativo=True)
        if modulo.liberado:
            return Response({})

        QTD = 3 if modulo.colaboracao == True else 1
        alunos = modulo.aluno_set.order_by('?').values_list('pk',flat=True)
        grupos = list(self.chunks(alunos,QTD))
        for g in grupos:
            grupo = Grupo()
            grupo.modulo = modulo
            grupo.save()
            Aluno.objects.filter(pk__in=g).update(grupo=grupo)
        modulo.liberado = True;
        modulo.save()
        return Response({'grupos':len(grupos)})


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
    queryset = Questao.objects.filter(modulos__ativo=True)
    serializer_class = QuestaoSerializer
