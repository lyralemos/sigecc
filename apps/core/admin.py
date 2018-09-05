from django.contrib import admin

from .models import *

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('__str__','colaboracao', 'competicao', 'ativo', 'liberado')


class PerguntaInline(admin.TabularInline):
    model = Pergunta


class QuestaoAdmin(admin.ModelAdmin):
    inlines = (PerguntaInline,)


class GrupoQuestaoInline(admin.TabularInline):
    model = GrupoQuestao


class GrupoAdmin(admin.ModelAdmin):
    inlines = [GrupoQuestaoInline]


class GrupoQuestaoAlunoInline(admin.TabularInline):
    model = GrupoQuestaoAluno


class GrupoQuestaoAmdin(admin.ModelAdmin):
    inlines = [GrupoQuestaoAlunoInline]

admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Aluno)
admin.site.register(PerfilPergunta)
admin.site.register(PerfilResposta)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Placar)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Pergunta)
admin.site.register(GrupoQuestao, GrupoQuestaoAmdin)
admin.site.register(GrupoQuestaoAluno)
admin.site.register(PerguntaFlow)
admin.site.register(RespostaFlow)
admin.site.register(Desafio)
admin.site.register(DesafioGrupo)
