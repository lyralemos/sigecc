from django.db.models import Sum
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Aluno, PerfilResposta, PerfilPergunta, Modulo, Grupo, Placar,\
    Questao, Pergunta, GrupoQuestao, GrupoQuestaoAluno, PerguntaFlow, RespostaFlow, \
    Desafio, DesafioGrupo


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', 'email', 'auth_token')


class PerfilPerguntaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PerfilPergunta
        fields = "__all__"


class PerfilRespostaSerializer(serializers.ModelSerializer):
    pergunta = serializers.StringRelatedField()

    class Meta(object):
        model = PerfilResposta
        fields = "__all__"


class AlunoSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=True)
    grupo = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(object):
        model = Aluno
        fields = "__all__"


class ModuloSerializer(serializers.ModelSerializer):
    alunos_count = serializers.SerializerMethodField()
    questoes_count = serializers.SerializerMethodField()
    grupos_count = serializers.SerializerMethodField()
    respostas_count = serializers.SerializerMethodField()
    placar = serializers.SerializerMethodField()

    def get_alunos_count(self, obj):
        return obj.aluno_set.count()

    def get_grupos_count(self, obj):
        return obj.grupo_set.count()

    def get_questoes_count(self, obj):
        return Pergunta.objects.count()

    def get_respostas_count(self, obj):
        return GrupoQuestao.objects.filter(
            grupo__modulo = obj
        ).exclude(resposta="").count()

    def get_placar(self, obj):
        return PlacarSerializer(Placar.objects.filter(grupo__modulo__ativo=True), many=True).data

    class Meta(object):
        model = Modulo
        fields = '__all__'

class SimpleGrupoSerializer(serializers.ModelSerializer):
    aluno_set = serializers.StringRelatedField(many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return Desafio.objects.aggregate(Sum('pontos'))['pontos__sum']

    class Meta(object):
        model = Grupo
        fields = ('id','__str__', 'foto', 'aluno_set', 'total', 'acertos', 'respondidas')


class PlacarSerializer(serializers.ModelSerializer):
    grupo = SimpleGrupoSerializer()
    marcar = serializers.SerializerMethodField()

    def get_marcar(self, obj):
        request = self.context.get('request')
        if request:
            if obj.grupo == request.user.aluno.grupo:
                return True
        return False

    class Meta(object):
        model = Placar
        fields = '__all__'


class PerguntaSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Pergunta
        exclude = ('resposta',)

class FullPerguntaSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Pergunta
        fields = '__all__'

class GrupoQuestaoAlunoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer()
    pergunta = PerguntaSerializer()

    class Meta(object):
        model = GrupoQuestaoAluno
        fields = ('id', 'aluno', 'pergunta', 'resposta', 'correto')


class QuestaoSerializer(serializers.ModelSerializer):
    pergunta = PerguntaSerializer()

    class Meta(object):
        model = Questao
        fields = ('id','pergunta')


class GrupoSerializer(serializers.ModelSerializer):
    aluno_set = serializers.StringRelatedField(many=True)
    questao = QuestaoSerializer()
    pontos = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    desafios = serializers.SerializerMethodField()
    proximo_desafio = serializers.SerializerMethodField()
    fotografo = AlunoSerializer()

    def get_questao(self, obj):
        return obj.questao.pk
    
    def get_pontos(self, obj):
        return obj.pontos
    
    def get_total(self, obj):
        return Desafio.objects.aggregate(Sum('pontos'))['pontos__sum']
    
    def get_desafios(self, obj):
        return DesafioGruopSerializer(obj.desafiogrupo_set.all(), many=True).data
    
    def get_proximo_desafio(self, obj):
        return DesafioSerializer(obj.proximo_desafio()).data

    class Meta(object):
        model = Grupo
        fields = ('id', '__str__', 'aluno_set', 'nome', 'modulo', 'questao', 
            'pontos', 'total', 'desafios', 'proximo_desafio', 'foto', 'fotografo')


class GrupoQuestaoSerializer(serializers.ModelSerializer):
    # grupo = GrupoSerializer()
    questao = QuestaoSerializer()
    respondedor = AlunoSerializer()
    grupo = SimpleGrupoSerializer()

    class Meta(object):
        model = GrupoQuestao
        fields = ('__all__')


class PerguntaFlowSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PerguntaFlow
        fields = "__all__"


class RespostaFlowSerializer(serializers.ModelSerializer):
    pergunta = serializers.StringRelatedField()

    class Meta(object):
        model = RespostaFlow
        fields = "__all__"


class DesafioSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Desafio
        fields = '__all__'


class DesafioGruopSerializer(serializers.ModelSerializer):
    desafio = DesafioSerializer()

    class Meta(object):
        model = DesafioGrupo
        fields = '__all__'