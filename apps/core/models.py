from django.db import models
from django.contrib.auth.models import User

class Modulo(models.Model):
    colaboracao = models.BooleanField(default=False)
    competicao = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    liberado = models.BooleanField(default=False)

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
    grupo = models.ForeignKey("Grupo", blank=True, null=True, on_delete=models.CASCADE)
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
        unique_together = ("pergunta", "resposta")


class Grupo(models.Model):
    nome = models.CharField(max_length=100, blank=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    def __str__(self):
        if self.aluno_set.count() == 1:
            return self.aluno_set.all()[0].nome
        return self.nome

class Placar(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)

    def acerto(self):
        self.pontos += 3
        self.save()

    def __str__(self):
        return str(self.pontos)


class Questao(models.Model):
    texto = models.TextField()
    modulos = models.ManyToManyField(Modulo)

    def __str__(self):
        return self.texto


RESPOSTA_CHOICE = (
    ("opcao1", "Opção 1"),
    ("opcao2", "Opção 2"),
    ("opcao3", "Opção 3"),
    ("opcao4", "Opção 4"),
    ("opcao5", "Opção 5"),
)


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
        return self.questao.texto


class AlunoResposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=6, choices=RESPOSTA_CHOICE)

    def save(self, *args, **kwargs):
        super(AlunoResposta, self).save(*args, **kwargs)
        placar, created = Placar.objects.get_or_create(grupo=self.aluno.grupo)
        if self.pergunta.resposta == self.resposta:
            placar.acerto()

    class Meta(object):
        unique_together = ('aluno', 'pergunta')
