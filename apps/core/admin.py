from django.contrib import admin

from .models import *

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('__str__','colaboracao', 'competicao', 'ativo', 'liberado', 'finalizado')


class QuestaoAdmin(admin.ModelAdmin):
    pass


class GrupoQuestaoInline(admin.TabularInline):
    model = GrupoQuestao


class GrupoAdmin(admin.ModelAdmin):
    inlines = [GrupoQuestaoInline]
    list_display = ('__str__', 'respondidas', 'acertos')
    list_filter = ('modulo',)


class GrupoQuestaoAlunoInline(admin.TabularInline):
    model = GrupoQuestaoAluno


class GrupoQuestaoAmdin(admin.ModelAdmin):
    list_display = ('__str__', 'grupo', 'questao', 'respondedor', 'resposta')


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'user_email', 'flow')
    search_fields = ('user__email', 'nome')
    list_filter = ('modulo',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'E-mail do Usuário'

    def flow(self, obj):
        qtd = obj.respostaflow_set.count()
        if qtd == 36:
            return True
        return False
    flow.boolean = True

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'resposta')


class DesafioGrupoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'desafio', 'grupo')


class RespostaFlowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'aluno')
    list_filter = ('aluno__modulo',)


class PlacarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'grupo')


class PerguntaFlowAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__')
    ordering = ('pk',)

admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(PerfilPergunta)
admin.site.register(PerfilResposta)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Placar, PlacarAdmin)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(GrupoQuestao, GrupoQuestaoAmdin)
admin.site.register(GrupoQuestaoAluno)
admin.site.register(PerguntaFlow, PerguntaFlowAdmin)
admin.site.register(RespostaFlow, RespostaFlowAdmin)
admin.site.register(Desafio)
admin.site.register(DesafioGrupo, DesafioGrupoAdmin)
