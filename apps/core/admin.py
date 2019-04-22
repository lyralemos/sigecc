from django.contrib import admin

from .models import *

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('__str__','colaboracao', 'competicao', 'ativo', 'liberado')


class QuestaoAdmin(admin.ModelAdmin):
    pass


class GrupoQuestaoInline(admin.TabularInline):
    model = GrupoQuestao


class GrupoAdmin(admin.ModelAdmin):
    inlines = [GrupoQuestaoInline]


class GrupoQuestaoAlunoInline(admin.TabularInline):
    model = GrupoQuestaoAluno


class GrupoQuestaoAmdin(admin.ModelAdmin):
    list_display = ('__str__', 'grupo', 'respondedor', 'resposta')


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'genero')


class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'resposta')


class DesafioGrupoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'desafio', 'grupo')


class RespostaFlowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'aluno')


admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(PerfilPergunta)
admin.site.register(PerfilResposta)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Placar)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(GrupoQuestao, GrupoQuestaoAmdin)
admin.site.register(GrupoQuestaoAluno)
admin.site.register(PerguntaFlow)
admin.site.register(RespostaFlow, RespostaFlowAdmin)
admin.site.register(Desafio)
admin.site.register(DesafioGrupo, DesafioGrupoAdmin)
