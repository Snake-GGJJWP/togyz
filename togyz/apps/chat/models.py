from django.db import models
from django.contrib.auth.models import User
from .consts import START_POS


class Game(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User)
    player_white = models.CharField(max_length=50, default='')
    player_black = models.CharField(max_length=50, default='')
    is_finished = models.BooleanField(default=False)
    winner = models.CharField(max_length=50, default='')
    loser = models.CharField(max_length=50, default='')
    color_turn = models.CharField(max_length=5, default='white')  # what's color the next turn (white/black)
    history = models.TextField(default='[]')  # json as a string
    current_position = models.TextField(default=START_POS)  # json as a string

    @property
    def is_started(self):
        if self.player_white and self.player_black:
            return True
        return False

    @property
    def winner_color(self):
        if self.winner == self.player_white:
            return 'white'
        elif self.winner == self.player_black:
            return 'black'
        else:
            return None

    @property
    def name(self):
        return '0' * max(0, 8 - len(str(self.id))) + str(self.id)

    def as_dict(self):
        return {
            'player_white': self.player_white,
            'player_black': self.player_black,
            'winner': self.winner,
            'winner_color': self.winner_color,
            'is_started': self.is_started,
            'is_finished': self.is_finished,
            'color_turn': self.color_turn
        }

    class Meta():
        ordering = ['-date']

    def __str__(self):
        return '{0} vs {1} | {2}'.format(self.player_white, self.player_black, self.date.strftime('%d.%m.%Y'))
