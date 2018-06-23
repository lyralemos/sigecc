from django.contrib import admin

from .models import *

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('__str__','colaboracao', 'competicao', 'ativo')

admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Aluno)
admin.site.register(PerfilPergunta)
admin.site.register(PerfilResposta)

admin.site.register(Grupo)
admin.site.register(Placar)
admin.site.register(Questao)
admin.site.register(Pergunta)
admin.site.register(AlunoResposta)
