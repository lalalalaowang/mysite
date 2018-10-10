from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request ,user)
                    return HttpResponse('login successful')
                else:
                    return HttpResponse('user not active')
            else:
                return HttpResponse('wrong username or password')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def index(request):
    return render(request, 'index.html', {'selected': 'index'})