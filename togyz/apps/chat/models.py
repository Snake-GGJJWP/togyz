from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User)
    player_white = models.CharField(max_length=50, default='')
    player_black = models.CharField(max_length=50, default='')
    history = models.TextField() # json as a string
    current_position = models.TextField() # json as a string