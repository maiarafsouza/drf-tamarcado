# Generated by Django 4.0.2 on 2022-04-22 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='status_cancelado',
            field=models.BooleanField(default=False),
        ),
    ]
