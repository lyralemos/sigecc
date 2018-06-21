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


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)
    perfil = PerfilRespostaSerializer(required=True, many=True)
    grupo = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(object):
        model = Aluno
        fields = "__all__"


class ModuloSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Modulo
        fields = '__all__'


class GrupoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Grupo
        fields = '__all__'


class PlacarSerializer(serializers.ModelSerializer):
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
