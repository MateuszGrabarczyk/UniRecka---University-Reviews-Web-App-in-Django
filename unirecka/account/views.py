from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():           
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('index')
            # return render(request, 'account/register_done.html', {
            #     'new_user': new_user
            # })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {
        'user_form': user_form
    })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('Account is blocked')
            else:
                return HttpResponse('Incorrect data.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')
