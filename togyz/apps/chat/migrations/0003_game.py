# Generated by Django 3.2.8 on 2021-11-09 06:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_delete_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('player_white', models.CharField(default='', max_length=50)),
                ('player_black', models.CharField(default='', max_length=50)),
                ('is_finished', models.BooleanField(default=False)),
                ('winner', models.CharField(default='', max_length=50)),
                ('loser', models.CharField(default='', max_length=50)),
                ('color_turn', models.CharField(default='white', max_length=5)),
                ('history', models.TextField(default='[]')),
                ('current_position', models.TextField(default='{"1": 9, "2": 9, "3": 9, "4": 9, "5": 9, "6": 9, "7": 9, "8": 9, "9": 9, "10": 9, "11": 9, "12": 9, "13": 9, "14": 9, "15": 9, "16": 9, "17": 9, "18": 9, "white_pool": 0, "black_pool": 0}')),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
