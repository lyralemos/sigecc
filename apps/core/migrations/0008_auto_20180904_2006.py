# Generated by Django 2.0.6 on 2018-09-04 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180904_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='acertos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='grupo',
            name='respondidas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='grupo',
            name='sequencia',
            field=models.IntegerField(default=0),
        ),
    ]
