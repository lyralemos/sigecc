from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets

from .models import Aluno, Modulo
from .serializers import AlunoSerializer, ModuloSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.filter(ativo=True)
    serializer_class = ModuloSerializer
