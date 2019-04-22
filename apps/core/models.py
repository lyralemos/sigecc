import random

from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

RESPOSTA_CHOICE = (
    ("opcao1", "Opção 1"),
    ("opcao2", "Opção 2"),
    ("opcao3", "Opção 3"),
    ("opcao4", "Opção 4"),
    ("opcao5", "Opção 5"),
)

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


class Modulo(models.Model):
    nome = models.CharField(max_length=200, blank=True)
    colaboracao = models.BooleanField(default=False)
    competicao = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    liberado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)

    def liberar(self):
        if self.ativo:
            QTD = 3 if self.colaboracao == True else 1
            alunos = self.aluno_set.order_by('?').values_list('pk',flat=True)
            for g in list(chunks(alunos,QTD)):
                alunos = Aluno.objects.filter(pk__in=g)
                fotografo = alunos.order_by('?').first()
                grupo = Grupo.objects.create(modulo = self, quantidade=QTD, fotografo=fotografo)
                alunos.update(grupo=grupo)
                grupo.atribuir()
            self.liberado = True;
            self.save()

    def finalizar(self):
        self.finalizado = True
        self.save()

    def save(self, *args, **kwargs):
        if self.ativo:
            qs = type(self).objects.filter(ativo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(ativo=False)
        super(Modulo, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.nome


class Aluno(models.Model):
    MASCULINO = "M"
    FEMININO = "F"
    GENERO_CHOICES = (
        (MASCULINO, "Masculino"),
        (FEMININO, "Feminino")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey("Grupo", blank=True, null=True, on_delete=models.SET_NULL)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    nascimento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)

    def __str__(self):
        return self.nome


class PerfilPergunta(models.Model):
    codigo = models.CharField(max_length=50)
    pergunta = models.CharField(max_length=300)

    def __str__(self):
        return self.pergunta


class PerfilResposta(models.Model):
    pergunta = models.ForeignKey(PerfilPergunta, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    resposta = models.IntegerField()

    def __str__(self):
        return self.pergunta.pergunta

    class Meta(object):
        unique_together = ("pergunta", "resposta", "aluno")


class Grupo(models.Model):
    nome = models.CharField(max_length=100, blank=True)
    quantidade = models.IntegerField()
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    questoes = models.ManyToManyField('Questao', through='GrupoQuestao')
    respondidas = models.IntegerField(default=0)
    acertos = models.IntegerField(default=0)
    sequencia = models.IntegerField(default=0)
    foto = models.ImageField(upload_to='fotos/%Y/%m/%d/', null=True)
    fotografo = models.ForeignKey(Aluno, related_name="fotografo", on_delete=models.CASCADE, blank=True, null=True)

    @property
    def questao(self):
        Questao = apps.get_model('core', 'Questao')
        try:
            return self.questoes.get(grupoquestao__ativo=True)
        except Questao.DoesNotExist:
            return None
    
    @property
    def perguntas_respondidas(self):
        return self.questoes.values_list('pergunta__pk', flat=True)

    def atribuir(self):
        GrupoQuestao = apps.get_model('core', 'GrupoQuestao')
        GrupoQuestao.objects.get(grupo=self, ativo=True).atribuir()

    def nova_questao(self):
        Questao = apps.get_model('core', 'Questao')
        Pergunta = apps.get_model('core', 'Pergunta')
        GrupoQuestao = apps.get_model('core', 'GrupoQuestao')
        Modulo = apps.get_model('core', 'Modulo')

        GrupoQuestao.objects.filter(grupo=self).update(ativo=False)

        # Só sorteia se o modulo não estiver finalizado
        if not self.modulo.finalizado:
            disponiveis = Pergunta.objects.exclude(pk__in=self.perguntas_respondidas).order_by('?')

            if disponiveis.count():
                questao = Questao.objects.create(pergunta=disponiveis.first())
                questao.modulos.add(self.modulo)

                grupo_questao = GrupoQuestao.objects.create(
                    grupo = self,
                    questao = questao,
                    ativo = True
                )
    
    def proximo_desafio(self):
        ultimo_desafio = self.desafiogrupo_set.all().last()
        try:
            if ultimo_desafio:
                return Desafio.objects.get(pk=ultimo_desafio.desafio.pk+1)
            return Desafio.objects.get(pk=1)
        except Desafio.DoesNotExist:
            return Desafio.objects.get(pk=1)
    
    @property
    def pontos(self):
        return Placar.objects.get(grupo=self).pontos

    def acertou(self):
        self.respondidas += 1
        self.acertos += 1
        self.sequencia += 1
        self.save()

    def errou(self):
        self.respondidas += 1
        self.sequencia = 0
        self.save()


    def __str__(self):
        if self.nome:
            return self.nome
        nomes = list(self.aluno_set.values_list('nome', flat=True))
        nomes = [i.split(' ')[0] for i in nomes]
        if len(nomes) > 1:
            return '{} e {}'.format(', '.join(nomes[:-1]), nomes[-1])
        return ','.join(nomes)


class Placar(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)

    def acerto(self):
        # self.pontos += 3
        self.save()

    def __str__(self):
        return str(self.pontos)

    class Meta(object):
        ordering = ('-pontos',)


class Questao(models.Model):
    # texto = models.TextField()
    modulos = models.ManyToManyField(Modulo)
    pergunta = models.ForeignKey('Pergunta', on_delete=models.CASCADE)


class Pergunta(models.Model):

    # questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    # titulo = models.CharField(max_length=200)
    enunciado = models.TextField(blank=True)
    opcao1 = models.CharField(max_length=200)
    opcao2 = models.CharField(max_length=200)
    opcao3 = models.CharField(max_length=200)
    opcao4 = models.CharField(max_length=200)
    opcao5 = models.CharField(max_length=200)
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE)

    def __str__(self):
        return self.enunciado


class GrupoQuestao(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE)
    respondedor = models.ForeignKey(Aluno, on_delete=models.CASCADE, blank=True, null=True)
    ativo = models.BooleanField()
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE, blank=True)

    @property
    def correto(self):
        if self.questao.pergunta.resposta == self.resposta:
            return True
        return False
    
    def atribuir(self):
        self.respondedor = self.grupo.aluno_set.order_by('?').first()
        self.save()


class GrupoQuestaoAluno(models.Model):
    grupo_questao = models.ForeignKey(GrupoQuestao, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE, blank=True)

    @property
    def correto(self):
        return self.pergunta.resposta == self.resposta


class PerguntaFlow(models.Model):
    pergunta = models.CharField(max_length=200)

    def __str__(self):
        return self.pergunta


class RespostaFlow(models.Model):
    pergunta = models.ForeignKey(PerguntaFlow, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    resposta = models.IntegerField()

    def __str__(self):
        return self.pergunta.pergunta

    class Meta(object):
        unique_together = ("pergunta", "resposta", "aluno")


class Desafio(models.Model):
    nome = models.CharField(max_length=200)
    pontos = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta(object):
        ordering = ('id',)


class DesafioGrupo(models.Model):
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def proximo(self):
        return DesafioGrupo.objects.get(pk=self.id+1)

    class Meta(object):
        unique_together = ("desafio", "grupo")
        ordering = ('desafio__pk',)


# Gera os tokens para os usuários automaticamente
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Grupo)
def define_questao(sender, instance=None, created=False, **kwargs):
    if created:
        instance.nova_questao()
        Placar.objects.create(grupo=instance)

@receiver(post_save, sender=GrupoQuestao)
def atribuir_questoes(sender, instance=None, created=False, **kwargs):
    if created:
        instance.atribuir()
    
    if instance.resposta:
        grupo = instance.grupo
        if instance.correto:
            grupo.acertou()
            acertos = [1,2,3,5,8,13,21,34]

            if grupo.acertos in acertos:
                DesafioGrupo.objects.create(grupo=grupo, desafio_id=acertos.index(grupo.acertos)+1)
            
        else:
            grupo.errou()
        
        
        grupo.nova_questao()

@receiver(post_save, sender=DesafioGrupo)
def desafio_grupo(sender, instance=None, created=False, **kwargs):
    p = Placar.objects.get(grupo=instance.grupo)
    p.pontos += instance.desafio.pontos
    p.save()
