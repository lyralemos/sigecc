# Generated by Django 2.0.6 on 2019-04-14 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190414_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questao',
            name='texto',
        ),
    ]
