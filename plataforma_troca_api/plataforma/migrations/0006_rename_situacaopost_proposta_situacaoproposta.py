# Generated by Django 4.2.6 on 2023-10-25 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0005_alter_post_tempo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposta',
            old_name='situacaoPost',
            new_name='situacaoProposta',
        ),
    ]
