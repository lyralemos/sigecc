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
                grupo = Grupo.objects.create(modulo = self, quantidade=QTD)
                Aluno.objects.filter(pk__in=g).update(grupo=grupo)
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

    @property
    def questao(self):
        Questao = apps.get_model('core', 'Questao')
        try:
            return self.questoes.get(grupoquestao__ativo=True)
        except Questao.DoesNotExist:
            return None
    
    @property
    def perguntas_respondidas(self):
        Pergunta = apps.get_model('core', 'Pergunta')

        respondidas = Pergunta.objects.none()
        for questao in self.questoes.all():
            respondidas = respondidas | questao.perguntas.all()
        
        return respondidas.values_list('pk', flat=True)

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
            
            questao = Questao.objects.create()
            questao.modulos.add(self.modulo)
            questao.perguntas.add(*disponiveis[:self.quantidade])

            grupo_questao = GrupoQuestao.objects.create(
                grupo = self,
                questao = questao,
                ativo = True
            )
            # count = len(disponiveis)
            # try:
            #     random_index = random.randint(0, count - 1)
            #     grupo_questao = GrupoQuestao.objects.create(
            #         grupo = self,
            #         questao = disponiveis[random_index],
            #         ativo = True
            #     )
            # except ValueError:
            #     pass

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
        nomes = self.aluno_set.values_list('nome', flat=True)
        nomes = [i.split(' ')[0] for i in nomes]
        return ', '.join(nomes)


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
    # texto = models.TextField()
    modulos = models.ManyToManyField(Modulo)
    perguntas = models.ManyToManyField('Pergunta')

    objects = QuestaoQuerySet.as_manager()

    # def __str__(self):
    #     return self.texto


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
    atribuicoes = models.ManyToManyField('Aluno', through='GrupoQuestaoAluno')
    ativo = models.BooleanField()

    @property
    def correto(self):
        for pergunta in self.grupoquestaoaluno_set.all():
            if not pergunta.correto:
                return False
        return True

    def atribuir(self):
        # perguntas = Pergunta.objects.filter(questao=self.questao).order_by('?')
        perguntas = self.questao.perguntas.all()
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

    class Meta(object):
        unique_together = ("desafio", "grupo")


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
    grupo_questao = instance.grupo_questao
    perguntas = GrupoQuestaoAluno.objects.filter(grupo_questao=grupo_questao)
    for pergunta in perguntas:
        if not pergunta.resposta:
            return None

    # O grupo acertou?
    grupo = grupo_questao.grupo
    if grupo_questao.correto:
        grupo.acertou()
    else:
        grupo.errou()

    # primeiro acerto
    if grupo.acertos == 1 and grupo.sequencia == 1:
        DesafioGrupo.objects.create(grupo=grupo,desafio_id=1)

    # 3 acertos em sequencia
    if grupo.sequencia == 3:
        DesafioGrupo.objects.create(grupo=grupo,desafio_id=2)

    # 5 acertos
    if grupo.acertos == 5:
        DesafioGrupo.objects.create(grupo=grupo,desafio_id=3)

    #todas as questoes
    total_questoes = Questao.objects.filter(modulos__id=grupo.modulo_id).count()
    if grupo.respondidas == total_questoes:
        DesafioGrupo.objects.create(grupo=grupo,desafio_id=4)

    instance.grupo_questao.grupo.nova_questao()

@receiver(post_save, sender=DesafioGrupo)
def desafio_grupo(sender, instance=None, created=False, **kwargs):
    p = Placar.objects.get(grupo=instance.grupo)
    p.pontos += instance.desafio.pontos
    p.save()
