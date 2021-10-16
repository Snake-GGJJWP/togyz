from django.shortcuts import redirect


def if_logged(func):
    def wrapper(request, **kwargs):
        if request.user.is_authenticated:
            return func(request, **kwargs)
        else:
            return redirect('login')
    return wrapper


def if_unlogged(func):
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated:
            return func(request, **kwargs)
        else:
            return redirect('lobby')
    return wrapper
