# Generated by Django 3.2.8 on 2021-10-21 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20211018_0143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.CharField(default='', max_length=50),
        ),
    ]