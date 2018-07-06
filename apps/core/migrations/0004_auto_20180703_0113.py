# Generated by Django 2.0.6 on 2018-07-03 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_grupoquestao'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoQuestaoAluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.CharField(choices=[('opcao1', 'Opção 1'), ('opcao2', 'Opção 2'), ('opcao3', 'Opção 3'), ('opcao4', 'Opção 4'), ('opcao5', 'Opção 5')], max_length=6)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Aluno')),
            ],
        ),
        migrations.AddField(
            model_name='grupo',
            name='questoes',
            field=models.ManyToManyField(through='core.GrupoQuestao', to='core.Questao'),
        ),
        migrations.AddField(
            model_name='grupoquestao',
            name='ativo',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoquestaoaluno',
            name='grupo_questao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.GrupoQuestao'),
        ),
        migrations.AddField(
            model_name='grupoquestaoaluno',
            name='pergunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pergunta'),
        ),
        migrations.AddField(
            model_name='grupoquestao',
            name='atribuicoes',
            field=models.ManyToManyField(through='core.GrupoQuestaoAluno', to='core.Aluno'),
        ),
    ]
