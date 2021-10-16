from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .decorators import if_logged, if_unlogged


@if_logged
def test(request, test):
    return HttpResponse(f'Hello {test}')


@if_unlogged
def registration_page(request):
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
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())

    return render(request, 'user_auth/registration.html', {'form': form})


@if_unlogged
def login_page(request):
    if request.method == "POST":
        print(type(request))
        username = request.POST.get('lg_username')
        password = request.POST.get('lg_password')

        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lobby')

    return render(request, 'user_auth/login.html')


@if_logged
def logout_user(request):
    logout(request)
    return redirect('login')
