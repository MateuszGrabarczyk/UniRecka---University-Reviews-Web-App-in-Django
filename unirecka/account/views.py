from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from universities.models import Review, Comment
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, "Podany adres email już istnieje.")   
                return render(request, 'account/register.html', {
                    'user_form': user_form
        }) 

        if User.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "Podana nazwa użytkownika już istnieje.")   
                return render(request, 'account/register.html', {
                    'user_form': user_form
                }) 

        if user_form.is_valid():      
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Pomyślnie zajerestrowano konto. Możesz już się zalogować.')
            send_mail(
                "Założono konto w aplikacji UniRecka",
                "Pomyślnie założono konto, teraz możesz się już zalogować",
                "stepowa28@gmail.com",
                [new_user.email],
                fail_silently=False,
            )
            return redirect('index')
        else:
            messages.error(request, "Podane dane są nieprawidłowe, spróbuj ponownie.")
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {
        'user_form': user_form
    })


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Pomyślnie zalogowano.')
                    return redirect('index')
            else:
                messages.error(request, "Podane dane są nieprawidłowe, spróbuj ponownie.")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request, user_id):
    if request.user.id != user_id:
        return redirect('index')
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        user.username = username
        user.email = email
        user.save()
        send_mail(
            "Zmiana danych konta w aplikacji UniRecka",
            "Pomyślnie zmieniono dane konta. Twoja nazwa użytkownika lub mail zostały zmienione.",
            "stepowa28@gmail.com",
            [user.email],
            fail_silently=False,
        )
        return redirect('profile', user_id=user_id)
    reviews = Review.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)

    return render(request, 'account/profile.html', {
        'user': user,
        'reviews': reviews,
        'comments': comments
        })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                "Zmiana hasła w aplikacji UniRecka",
                "Pomyślnie zmieniono hasło do konta. Zostałeś wylogowany, zaloguj się ponownie, tym razem z nowym hasłem.",
                "stepowa28@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return redirect('profile', user_id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})