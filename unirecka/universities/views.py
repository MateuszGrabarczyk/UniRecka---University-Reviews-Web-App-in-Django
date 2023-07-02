from django.shortcuts import render
from .models import University

def university_list(request):
    universities = University.objects.all()
    return render(request, 'universities/university_list.html', {
        'universities': universities
    })