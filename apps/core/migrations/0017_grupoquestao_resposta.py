# Generated by Django 2.0.6 on 2019-04-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20190420_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupoquestao',
            name='resposta',
            field=models.CharField(blank=True, choices=[('opcao1', 'Opção 1'), ('opcao2', 'Opção 2'), ('opcao3', 'Opção 3'), ('opcao4', 'Opção 4'), ('opcao5', 'Opção 5')], max_length=6),
        ),
    ]
