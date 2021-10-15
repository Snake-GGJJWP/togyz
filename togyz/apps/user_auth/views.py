from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

def registration(request):
    form = CreateUserForm()
    print(request.method)

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {user}')
            return redirect('login')
        else:
            messages.error(request, f'Something went wrong')


    return render(request, 'user_auth/registration.html', {'form': form})


def login(request):
    if request.method == "POST":
        print(type(request))
        username = request.get('lg_username')
        password = request.get('lg_password')

        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lobby')

    return render(request, 'user_auth/login.html')
