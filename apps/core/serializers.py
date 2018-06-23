from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Aluno, PerfilResposta, PerfilPergunta, Modulo, Grupo, Placar,\
    Questao, Pergunta


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


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
    user = UserSerializer(required=True)
    perfil = PerfilRespostaSerializer(required=True, many=True)
    grupo = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(object):
        model = Aluno
        fields = "__all__"


class ModuloSerializer(serializers.ModelSerializer):
    alunos_count = serializers.SerializerMethodField()
    questoes_count = serializers.SerializerMethodField()
    grupos_count = serializers.SerializerMethodField()
    placar = serializers.SerializerMethodField()

    def get_alunos_count(self, obj):
        return Aluno.objects.filter(grupo__modulo__ativo=True).count()

    def get_grupos_count(self, obj):
        return obj.grupo_set.count()

    def get_questoes_count(self, obj):
        return obj.questao_set.count()

    def get_placar(self, obj):
        return PlacarSerializer(Placar.objects.filter(grupo__modulo__ativo=True), many=True).data

    class Meta(object):
        model = Modulo
        fields = '__all__'


class GrupoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Grupo
        fields = '__all__'


class PlacarSerializer(serializers.ModelSerializer):
    grupo = serializers.StringRelatedField()

    class Meta(object):
        model = Placar
        fields = '__all__'


class PerguntaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Pergunta
        exclude = ('questao',)


class QuestaoSerializer(serializers.ModelSerializer):
    pergunta_set = PerguntaSerializer(required=True, many=True)

    class Meta(object):
        model = Questao
        fields = ('id', 'texto', 'pergunta_set')
