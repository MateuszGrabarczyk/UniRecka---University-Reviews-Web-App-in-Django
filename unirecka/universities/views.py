from django.shortcuts import render
from django.views.generic import DetailView
from .models import University

def university_list(request):
    name = request.GET.get('name', '')
    city = request.GET.get('city', '')
    voivodeship = request.GET.get('voivodeship', '')
    universities = University.objects.all()
    cities = universities.values_list('city', flat=True).distinct()
    if name != '':
        universities = universities.filter(name__icontains=name)
    if city != '':
        universities = universities.filter(city__icontains=city)
    if voivodeship != '':
        universities = universities.filter(voivodeship__icontains=voivodeship)
    
    return render(request, 'universities/university_list.html', {
        'universities': universities,
        'name_value': name,
        'city_value': city,
        'voivodeship_value': voivodeship,
        'cities': cities
    })

class UniversityDetailView(DetailView):
    model = University
    template_name = 'universities/university_detail.html'  # Replace with your desired template name
    context_object_name = 'university'