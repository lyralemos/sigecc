# Generated by Django 2.0.6 on 2018-07-01 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180701_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoQuestao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Grupo')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Questao')),
            ],
        ),
    ]
