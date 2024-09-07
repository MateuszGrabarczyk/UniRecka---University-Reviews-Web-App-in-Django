from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from universities.models import Comment, Review

from .forms import LoginForm, UserRegistrationForm
from .utils import (
    handle_username_and_email_update,
    send_password_change_email,
    send_profile_change_email,
    send_registration_email,
    validate_registration_data,
)


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if not validate_registration_data(request, user_form):
            return render(request, "account/register.html", {"user_form": user_form})

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()

            messages.success(
                request, "Pomyślnie zajerestrowano konto. Możesz już się zalogować."
            )

            send_registration_email(new_user)

            return redirect("index")
        else:
            messages.error(request, "Podane dane są nieprawidłowe, spróbuj ponownie.")
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])

            if user is None:
                try:
                    if not User.objects.get(username=cd["username"]).is_active:
                        messages.error(
                            request,
                            "Twoje konto jest nieaktywne. Jeśli chcesz je ponownie aktywować, skontaktuj się z administratorem pod adresem email: stepowa28@gmail.com",
                        )
                        return render(request, "account/login.html", {"form": form})
                    else:
                        messages.error(
                            request, "Podane dane są nieprawidłowe, spróbuj ponownie."
                        )
                except User.DoesNotExist:
                    messages.error(
                        request, "Podane dane są nieprawidłowe, spróbuj ponownie."
                    )
            else:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Pomyślnie zalogowano.")
                    return redirect("index")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("index")


@login_required
def profile(request):
    user = request.user
    reviews = Review.objects.filter(user=user, active=True)
    comments = Comment.objects.filter(user=user, active=True)

    if request.method == "POST":
        if handle_username_and_email_update(request, user):
            send_profile_change_email(user)
            messages.success(request, "Twoje dane konta zostały zmienione.")
        return redirect("profile")

    return render(
        request,
        "account/profile.html",
        {"user": user, "reviews": reviews, "comments": comments},
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            send_password_change_email(user)
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "account/change_password.html", {"form": form})


@login_required
def deactivate_confirm(request):
    return render(request, "account/deactivate_confirm.html")


@login_required
def deactivate_account(request):
    user = request.user

    Review.objects.filter(user=user).update(active=False)
    Comment.objects.filter(user=user).update(active=False)

    user.is_active = False
    user.save()
    logout(request)

    return render(request, "account/deactivate_account.html")
