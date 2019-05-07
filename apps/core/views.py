import base64, uuid

from django.core.files.base import ContentFile
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render
from django.db import IntegrityError

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Aluno, Modulo, PerfilPergunta, PerfilResposta, Grupo, \
    Placar, Questao, GrupoQuestao, Pergunta, GrupoQuestaoAluno, PerguntaFlow, \
    RespostaFlow, Desafio, DesafioGrupo
from .serializers import AlunoSerializer, ModuloSerializer, \
    PerfilPerguntaSerializer, GrupoSerializer, PlacarSerializer, \
    QuestaoSerializer, GrupoQuestaoAlunoSerializer, PerguntaFlowSerializer, \
    DesafioSerializer, FullPerguntaSerializer, GrupoQuestaoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def create(self, request):
        try:
            user = User.objects.create_user(request.data['cpf'],request.data['email'],request.data['cpf'])
        except IntegrityError:
            return Response({'errors':['Esse usuário já existe']}, status=status.HTTP_400_BAD_REQUEST)
        aluno = Aluno.objects.create(
            nome = request.data['nome'],
            nascimento = request.data['nascimento'],
            genero = request.data['genero'],
            user = user,
            modulo = Modulo.objects.get(ativo=True)
        )

        return Response({'token':user.auth_token.key})

    @action(methods=['post'], detail=False)
    def perfil(self, request):
        aluno = request.user.aluno
        for pergunta,resposta in request.data['respostas'].items():
            PerfilResposta.objects.create(
                aluno = aluno,
                pergunta = PerfilPergunta.objects.get(pk=pergunta),
                resposta = resposta
            )
        return Response({'result':True})

    @action(methods=['post'], detail=False)
    def flow(self, request):
        aluno = request.user.aluno
        for pergunta,resposta in request.data['respostas'].items():
            RespostaFlow.objects.create(
                aluno = aluno,
                pergunta_id = pergunta,
                resposta = resposta
            )
        DesafioGrupo.objects.create(grupo=aluno.grupo, desafio_id=5)
        return Response({'result':True})


class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer

    @action(methods=['get'], detail=False)
    def ativo(self, request):
        if type(request.user) != AnonymousUser:
            if request.user.aluno.modulo.ativo == False:
                return Response({'error': 'Aluno de outro modulo'})
        try:
            modulo = Modulo.objects.get(ativo=True)
            serializer = self.get_serializer(modulo)
            return Response(serializer.data)
        except Modulo.DoesNotExist:
            return Response({})

    @action(methods=['get'], detail=False)
    def liberar(self, request):
        modulo = Modulo.objects.get(ativo=True)
        modulo.liberar()
        return Response({'result':'success'})

    @action(methods=['get'], detail=False)
    def finalizar(self, request):
        modulo = Modulo.objects.get(ativo=True)
        modulo.finalizar()
        return Response({'result': 'success'})


class PerfilPerguntaViewSet(viewsets.ModelViewSet):
    # queryset = PerfilPergunta.objects.all()
    serializer_class = PerfilPerguntaSerializer

    def get_queryset(self):
        respondidas = PerfilResposta.objects.filter(aluno__user=self.request.user).values_list('pergunta',flat=True)
        return PerfilPergunta.objects.exclude(id__in=list(respondidas))

class PerguntaViewSet(viewsets.ModelViewSet):
    serializer_class = FullPerguntaSerializer
    queryset = Pergunta.objects.all()


class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.filter(modulo__ativo = True)
    serializer_class = GrupoSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def perguntas(self, request):
        grupo = request.user.aluno.grupo
        try:
            grupo_questao = GrupoQuestao.objects.get(grupo=grupo, ativo=True)
            
            return Response({
                'aluno': request.user.aluno.pk,
                'grupo_questao': GrupoQuestaoSerializer(grupo_questao).data,
            })
        except GrupoQuestao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def status(self, request):
        data = {
            'aluno': request.user.aluno.pk,
            'grupo': GrupoSerializer(request.user.aluno.grupo).data
        }
        return Response(data)

    @action(methods=['get'], detail=False)
    def respondido(self, request):
        gq = GrupoQuestao.objects.get(pk=request.query_params['id'])
        # gq = GrupoQuestao.objects.get(grupo=request.user.aluno.grupo, ativo=True)
        if gq.resposta:
            return Response({'result': True})
        return Response({'result': False})

    @action(methods=['post'], detail=False)
    def responder(self, request):
        grupo_questao = GrupoQuestao.objects.get(pk=request.data['grupo_questao'])
        grupo_questao.resposta = request.data['resposta']
        grupo_questao.save()
        if grupo_questao.correto:
            Placar.objects.get(grupo=grupo_questao.grupo).acerto()
        return Response({'result': grupo_questao.correto})
    
    @action(methods=['patch'], detail=False)
    def foto(self, request):
        grupo = request.user.aluno.grupo
        data = request.data['foto']
        format, imgstr = data.split(';base64,') # format ~= data:image/X,
        ext = format.split('/')[-1] # guess file extension
        id = uuid.uuid4()
        grupo.foto = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        grupo.save()
        return Response({'result':True})


class PlacarViewSet(viewsets.ModelViewSet):
    queryset = Placar.objects.filter(grupo__modulo__ativo = True).order_by('-pontos')
    serializer_class = PlacarSerializer


class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.filter(modulos__ativo=True)
    serializer_class = QuestaoSerializer

    @action(methods=['get'], detail=False)
    def atual(self, request):
        grupo_questao = GrupoQuestao.objects.get(grupo__aluno=request.user.aluno)
        serializer = self.get_serializer(grupo_questao.questao)
        return Response(serializer.data)


class PerguntaFlowViewSet(viewsets.ModelViewSet):
    queryset = PerguntaFlow.objects.all()
    serializer_class = PerguntaFlowSerializer

    def list(self, request):
        aluno = request.user.aluno
        respondidas = RespostaFlow.objects.filter(aluno__pk=aluno.pk).count()
        if respondidas:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super(PerguntaFlowViewSet, self).list(request)


class DesafioViewSet(viewsets.ModelViewSet):
    queryset = Desafio.objects.all()
    serializer_class = DesafioSerializer

    @action(methods=['get'], detail=False)
    def grupo(self, request):
        desafios = DesafioGrupo.objects.filter(grupo=request.user.aluno.grupo).values_list('desafio_id', flat=True)
        return Response({'desafios': desafios})
