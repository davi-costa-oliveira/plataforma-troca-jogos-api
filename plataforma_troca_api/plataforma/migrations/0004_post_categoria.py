# Generated by Django 4.2.6 on 2023-10-22 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0003_rename_nome_situacaopost_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='plataforma.categoria'),
            preserve_default=False,
        ),
    ]