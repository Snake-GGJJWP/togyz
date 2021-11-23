from django.shortcuts import render, redirect
from user_auth.decorators import if_logged
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Game

from .consts import WHITE, BLACK


@if_logged
def lobby(request):
    return render(request, 'chat/lobby.html')


@if_logged
def room(request, room_name):
    # GAME MODEL ALTERED. NEED TO CHANGE THE LOGIC IN THIS FUNCTION AND consumers.GameConsumer.connect and consumers.GameConsumer.make_move
    game_id = _name_to_id(room_name)
    try:
        game = Game.objects.filter(id=game_id).first()
    except IndexError:
        return redirect('lobby')
    player = User.objects.filter(username=request.user.username).first()

    print(game.player_white)
    print(game.player_black)
    print(player)

    if player not in game.players.all():
        if not game.player_white:
            game.players.add(player)
            game.player_white = player.username
            color = WHITE
            print("HE'S A PLAYER AND WE DIDNT KNOW IT. HE'S WHITE")
        elif not game.player_black:
            game.players.add(player)
            game.player_black = player.username
            color = BLACK
            print("HE'S A PLAYER AND WE DIDNT KNOW IT. HE'S BLACK")
        else:
            color = 'spec'
    else:
        print("HE'S A PLAYER AND WE KNOW IT")
        if game.player_white == player.username:
            color = WHITE
            print("HE'S WHITE")
        else:
            print("HE'S BLACK")
            color = BLACK
    game.save()
    if color == WHITE:
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


def _name_to_id(name):
    i = 0
    while name[i] == '0':
        i += 1
    game_id = name[i:]
    return game_id


@if_logged
def waiting_room(request):
    if request.method == "GET":
        return redirect('lobby')
    print(request.POST)
    player = User.objects.filter(username=request.user.username).first()
    if request.POST.get('white'):
        game = Game(player_white=player.username)
    elif request.POST.get('black'):
        game = Game(player_black=player.username)
    else:
        messages.warning(request, "You sent incomplete game settings")
        return redirect("lobby")
    game.save()
    game.players.add(player)
    print(game)
    return redirect('room', room_name=game.name)
    # return render(request, 'chat/test.html')


def test(request):
    return render(request, 'chat/test.html')
