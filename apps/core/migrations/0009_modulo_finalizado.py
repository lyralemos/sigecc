# Generated by Django 2.0.6 on 2018-09-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180904_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
    ]
