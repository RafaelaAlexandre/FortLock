# Generated by Django 4.2.6 on 2023-11-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fortlock_app', '0004_cofre_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cofre',
            name='nome',
            field=models.CharField(default='Cofre', max_length=30),
        ),
    ]
