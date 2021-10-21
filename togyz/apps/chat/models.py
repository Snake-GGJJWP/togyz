from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User)
    player_white = models.CharField(max_length=50, default='')
    player_black = models.CharField(max_length=50, default='')
    is_finished = models.BooleanField(null=True)
    winner = models.CharField(max_length=50, default='')
    loser = models.CharField(max_length=50, default='')
    color_turn = models.CharField(max_length=5, default='white')  # what's color the next turn (white/black)
    history = models.TextField()  # json as a string
    current_position = models.TextField()  # json as a string

    @property
    def is_started(self):
        if self.player_white and self.player_black:
            return True
        return False

    class Meta():
        ordering = ['-date']

    def __str__(self):
        return '{0} vs {1} | {2}'.format(self.player_white, self.player_black, self.date.strftime('%d.%m.%Y'))
