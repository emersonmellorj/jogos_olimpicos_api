# Generated by Django 2.2.9 on 2020-04-23 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogos', '0002_results_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='stage',
            field=models.CharField(max_length=100),
        ),
    ]
