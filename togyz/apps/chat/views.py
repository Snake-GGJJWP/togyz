from django.shortcuts import render

# Create your views here.


def lobby(request):
    return render(request, 'chat/lobby.html')


def room(request, room_name, color):
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
        'you': you
    })


def test(request):
    return render(request, 'chat/test.html')
