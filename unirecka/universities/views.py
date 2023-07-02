from django.shortcuts import render
from django.views.generic import DetailView
from .models import University

def university_list(request):
    universities = University.objects.all()
    return render(request, 'universities/university_list.html', {
        'universities': universities
    })

class UniversityDetailView(DetailView):
    model = University
    template_name = 'universities/university_detail.html'  # Replace with your desired template name
    context_object_name = 'university'