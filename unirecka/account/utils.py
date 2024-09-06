from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from universities.utils import check_if_has_cursed_words


def validate_registration_data(request, user_form):
    """
    Validates the registration form data.
    Returns False if there are validation errors; True if the data is valid.
    """
    if User.objects.filter(email=request.POST["email"]).exists():
        messages.error(request, "Podany adres email już istnieje.")
        return False

    if User.objects.filter(username=request.POST["username"]).exists():
        messages.error(request, "Podana nazwa użytkownika już istnieje.")
        return False

    if request.POST["password"] != request.POST["password2"]:
        messages.error(request, "Podane hasła nie są identyczne.")
        return False

    if len(request.POST["password"]) < 8:
        messages.error(request, "Podane hasło musi mieć co najmniej 8 znaków.")
        return False

    if check_if_has_cursed_words(request.POST["username"].split()):
        messages.error(
            request,
            "Twoja nazwa użytkownika zawiera niedozwolone słowo, spróbuj ponownie.",
        )
        return False

    return True


def send_registration_email(user):
    """Sends a registration email."""
    send_mail(
        "Założono konto w aplikacji UniRecka",
        "Pomyślnie założono konto, teraz możesz się już zalogować",
        "stepowa28@gmail.com",
        [user.email],
        fail_silently=False,
    )


def send_profile_change_email(user):
    """Sends an email after profile data has been updated."""
    send_mail(
        "Zmiana danych konta w aplikacji UniRecka",
        "Pomyślnie zmieniono dane konta. Twoja nazwa użytkownika lub mail zostały zmienione.",
        "stepowa28@gmail.com",
        [user.email],
        fail_silently=False,
    )


def send_password_change_email(user):
    """Sends an email after a password has been changed."""
    send_mail(
        "Zmiana hasła w aplikacji UniRecka",
        "Pomyślnie zmieniono hasło do konta. Zostałeś wylogowany, zaloguj się ponownie, tym razem z nowym hasłem.",
        "stepowa28@gmail.com",
        [user.email],
        fail_silently=False,
    )


def handle_username_and_email_update(request, user):
    """
    Handles the logic for updating the username and email.
    Returns True if successful; otherwise, False.
    """
    username = request.POST["username"]
    email = request.POST["email"]

    if User.objects.exclude(pk=user.id).filter(username=username).exists():
        messages.error(request, "Podana nazwa użytkownika już istnieje.")
        return False

    if User.objects.exclude(pk=user.id).filter(email=email).exists():
        messages.error(request, "Podany adres email już istnieje.")
        return False

    if check_if_has_cursed_words(username.split()):
        messages.error(
            request,
            "Twoja nazwa użytkownika zawiera niedozwolone słowo, spróbuj ponownie.",
        )
        return False

    user.username = username
    user.email = email
    user.save()

    return True
