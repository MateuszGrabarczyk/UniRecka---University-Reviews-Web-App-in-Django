from django.shortcuts import render

from universities.models import University


def index(request):
    jg = University.objects.filter(name="Uniwersytet Jagielloński w Krakowie").first()
    uw = University.objects.filter(name="Uniwersytet Warszawski").first()
    agh = University.objects.filter(
        name="Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie"
    ).first()
    return render(request, "main/index.html", {"jg": jg, "uw": uw, "agh": agh})


def about(request):
    return render(request, "main/about.html")
