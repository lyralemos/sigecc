from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render

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
    DesafioSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def create(self, request):
        user = User.objects.create_user(request.data['cpf'],'fake@email.com',request.data['cpf'])
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
    queryset = Modulo.objects.filter(ativo=True)
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


class PerfilPerguntaViewSet(viewsets.ModelViewSet):
    # queryset = PerfilPergunta.objects.all()
    serializer_class = PerfilPerguntaSerializer

    def get_queryset(self):
        respondidas = PerfilResposta.objects.filter(aluno__user=self.request.user).values_list('pergunta',flat=True)
        print(list(respondidas))
        return PerfilPergunta.objects.exclude(id__in=list(respondidas))


class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.filter(modulo__ativo = True)
    serializer_class = GrupoSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def perguntas(self, request):
        questao = request.user.aluno.grupo.questao
        perguntas_aluno = GrupoQuestaoAluno.objects.filter(
            grupo_questao__grupo = request.user.aluno.grupo,
            grupo_questao__ativo=True
        )
        serializer_questao = QuestaoSerializer(questao)
        serializer_perguntas = GrupoQuestaoAlunoSerializer(perguntas_aluno, many=True)

        return Response({
            'aluno': request.user.aluno.pk,
            'grupo': request.user.aluno.grupo.pk,
            'questao': serializer_questao.data,
            'perguntas': serializer_perguntas.data
        })

    @action(methods=['get'], detail=False)
    def status(self, request):
        questao_id = request.query_params.get('questao')
        if request.user.aluno.grupo.questao.pk == int(questao_id):
            return Response({'result':False})
        return Response({'result':True})


    @action(methods=['post'], detail=False)
    def responder(self, request):
        questao_aluno = GrupoQuestaoAluno.objects.get(pk=request.data['questao_aluno'])
        questao_aluno.resposta = request.data['resposta']
        questao_aluno.save()
        if questao_aluno.correto:
            Placar.objects.get(grupo=questao_aluno.grupo_questao.grupo).acerto()
        return Response({'result': questao_aluno.correto})


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


class DesafioViewSet(viewsets.ModelViewSet):
    queryset = Desafio.objects.all()
    serializer_class = DesafioSerializer

    @action(methods=['get'], detail=False)
    def grupo(self, request):
        desafios = DesafioGrupo.objects.filter(grupo=request.user.aluno.grupo).values_list('desafio_id', flat=True)
        return Response({'desafios': desafios})
