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
    colaboracao = models.BooleanField(default=False)
    competicao = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    liberado = models.BooleanField(default=False)

    def liberar(self):
        if self.ativo:
            QTD = 3 if self.colaboracao == True else 1
            alunos = self.aluno_set.order_by('?').values_list('pk',flat=True)
            for g in list(chunks(alunos,QTD)):
                grupo = Grupo.objects.create(
                    modulo = self
                )
                Aluno.objects.filter(pk__in=g).update(grupo=grupo)
                grupo.atribuir()
            self.liberado = True;
            self.save()

    def save(self, *args, **kwargs):
        if self.ativo:
            qs = type(self).objects.filter(ativo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(ativo=False)
        super(Modulo, self).save(*args, **kwargs)


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
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    questoes = models.ManyToManyField('Questao', through='GrupoQuestao')

    @property
    def questao(self):
        Questao = apps.get_model('core', 'Questao')
        try:
            return self.questoes.get(grupoquestao__ativo=True)
        except Questao.DoesNotExist:
            return None

    def atribuir(self):
        GrupoQuestao = apps.get_model('core', 'GrupoQuestao')
        GrupoQuestao.objects.get(grupo=self, ativo=True).atribuir()

    def nova_questao(self):
        Questao = apps.get_model('core', 'Questao')
        GrupoQuestao = apps.get_model('core', 'GrupoQuestao')

        GrupoQuestao.objects.filter(grupo=self).update(ativo=False)

        respondidas = self.questoes.values_list('pk', flat=True)
        disponiveis = Questao.objects.filter(modulos=self.modulo).exclude(id__in=respondidas)
        count = len(disponiveis)
        try:
            random_index = random.randint(0, count - 1)
            grupo_questao = GrupoQuestao.objects.create(
                grupo = self,
                questao = disponiveis[random_index],
                ativo = True
            )
        except ValueError:
            pass

    def __str__(self):
        return ', '.join(self.aluno_set.values_list('nome', flat=True))


class Placar(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)

    def acerto(self):
        self.pontos += 3
        self.save()

    def __str__(self):
        return str(self.pontos)

    class Meta(object):
        ordering = ('-pontos',)

class QuestaoQuerySet(models.query.QuerySet):

    def aleatoria(self, modulo):
        return self.filter(modulos=modulo).order_by('?')[0]


class Questao(models.Model):
    texto = models.TextField()
    modulos = models.ManyToManyField(Modulo)

    objects = QuestaoQuerySet.as_manager()

    def __str__(self):
        return self.texto


class Pergunta(models.Model):

    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    opcao1 = models.CharField(max_length=200)
    opcao2 = models.CharField(max_length=200)
    opcao3 = models.CharField(max_length=200)
    opcao4 = models.CharField(max_length=200)
    opcao5 = models.CharField(max_length=200)
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE)

    def __str__(self):
        return self.titulo


class GrupoQuestao(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    questao = models.ForeignKey('Questao', on_delete=models.CASCADE)
    atribuicoes = models.ManyToManyField('Aluno', through='GrupoQuestaoAluno')
    ativo = models.BooleanField()

    def atribuir(self):
        perguntas = Pergunta.objects.filter(questao=self.questao).order_by('?')
        alunos = self.grupo.aluno_set.all()
        for aluno,pergunta in zip(alunos,perguntas):
            GrupoQuestaoAluno.objects.create(
                grupo_questao = self,
                aluno = aluno,
                pergunta = pergunta
            )


class GrupoQuestaoAluno(models.Model):
    grupo_questao = models.ForeignKey(GrupoQuestao, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE, blank=True)

    @property
    def correto(self):
        return self.pergunta.resposta == self.resposta


class AlunoResposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE)

    @property
    def acertou(self):
        return self.pergunta.resposta == self.resposta

    def save(self, *args, **kwargs):
        super(AlunoResposta, self).save(*args, **kwargs)
        placar, created = Placar.objects.get_or_create(grupo=self.aluno.grupo)
        if self.acertou:
            placar.acerto()

        questao = self.pergunta.questao
        if questao.pergunta_set.count() == 1:
            respondidas = AlunoResposta.objects.filter(aluno=self.aluno).values_list('pergunta',flat=True)
            questoes = Pergunta.objects.exclude(pk__in=respondidas).values_list(flat=True).distinct()
            count = len(questoes)
            random_index = random.randint(0, count - 1)
            questao = questoes[random_index]
            gq = GrupoQuestao.objects.get(grupo = self.aluno.grupo)
            gq.questao_id = questao
            gq.save()


    class Meta(object):
        unique_together = ('aluno', 'pergunta')


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

@receiver(post_save, sender=GrupoQuestaoAluno)
def verifica_respostas(sender, instance=None, created=False, **kwargs):
    perguntas = GrupoQuestaoAluno.objects.filter(grupo_questao=instance.grupo_questao)
    for pergunta in perguntas:
        if not pergunta.resposta:
            return None
    instance.grupo_questao.grupo.nova_questao()
