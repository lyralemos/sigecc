from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Aluno, PerfilResposta, Modulo


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PerfilRespostaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PerfilResposta
        fields = "__all__"


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)
    perfil = PerfilRespostaSerializer(required=True, many=True)

    class Meta(object):
        model = Aluno
        fields = "__all__"


class ModuloSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Modulo
        fields = '__all__'
