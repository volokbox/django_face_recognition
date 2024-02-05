# Generated by Django 5.0.1 on 2024-01-29 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_escola'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('ID_Turma', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('ID_Aluno', models.BigAutoField(primary_key=True, serialize=False)),
                ('Nome', models.CharField(max_length=100)),
                ('ID_Turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.turma')),
            ],
        ),
    ]