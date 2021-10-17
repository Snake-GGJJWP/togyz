from django.shortcuts import render, redirect
from user_auth.decorators import if_logged
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Game

from binascii import hexlify
from datetime import datetime


@if_logged
def lobby(request):
    return render(request, 'chat/lobby.html')


@if_logged
def room(request, room_name):
    try:
        game = Game.objects.filter(name=room_name)[0]
    except IndexError:
        return redirect('lobby')
    player = User.objects.filter(username=request.user.username)[0]

    print(game.player_white)
    print(game.player_black)
    print(player)

    if player not in game.players.all():
        if not game.player_white:
            game.players.add(player)
            game.player_white = player.username
            color = 'white'
            print("HE'S A PLAYER AND WE DIDNT KNOW IT. HE'S WHITE")
        elif not game.player_black:
            game.players.add(player)
            game.player_black = player.username
            color = 'black'
            print("HE'S A PLAYER AND WE DIDNT KNOW IT. HE'S BLACK")
        else:
            color = 'spec'
    else:
        print("HE'S A PLAYER AND WE KNOW IT")
        if game.player_white == player.username:
            color = 'white'
            print("HE'S WHITE")
        else:
            print("HE'S BLACK")
            color = 'black'
    game.save()
    if color == 'white':
        opponent = list(range(18, 9, -1))
        you = list(range(1, 10))
    else:
        opponent = list(range(9, 0, -1))
        you = list(range(10, 19))
    print(opponent, you)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'color': color,
        'opponent': opponent,
        'you': you,
    })


@if_logged
def waiting_room(request):
    if request.method == "GET":
        return redirect('lobby')
    print(request.POST)
    game_name = hexlify(request.user.username.encode('utf-8') + datetime.now().strftime("%m-%d-%Y-%H-%M-%S").encode('utf-8'))
    game_name = game_name.decode('utf-8')
    player = User.objects.filter(username=request.user.username)[0]
    game = Game(name=game_name, history='', current_position='')
    if request.POST.get('white'):
        game = Game(name=game_name, player_white=player.username, history='', current_position='')
    else:
        game = Game(name=game_name, player_black=player.username, history='', current_position='')
    game.save()
    game.players.add(player)
    print(game)
    return redirect('room', room_name=game_name)
    # return render(request, 'chat/test.html')


def test(request):
    return render(request, 'chat/test.html')
