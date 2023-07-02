from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from .models import Review, University

def university_list(request):
    name = request.GET.get('name', '')
    city = request.GET.get('city', '')
    voivodeship = request.GET.get('voivodeship', '')
    universities = University.objects.all()
    cities = universities.values_list('city', flat=True).distinct()
    voivodeships = universities.values_list('voivodeship', flat=True).distinct()
    if name != '':
        universities = universities.filter(name__icontains=name)
    if city != '':
        universities = universities.filter(city=city)
    if voivodeship != '':
        universities = universities.filter(voivodeship=voivodeship)
    
    return render(request, 'universities/university_list.html', {
        'universities': universities,
        'name_value': name,
        'city_value': city,
        'voivodeship_value': voivodeship,
        'cities': cities,
        'voivodeships': voivodeships
    })

class UniversityDetailView(DetailView):
    model = University
    template_name = 'universities/university_detail.html'  # Replace with your desired template name
    context_object_name = 'university'

class ReviewCreateView(CreateView):
    model = Review
    template_name = 'universities/review_create.html'
    fields = ['title', 'description', 'rating']
    success_url = reverse_lazy('university_list')

    def form_valid(self, form):
        university = get_object_or_404(University, id=self.kwargs['university_id'])
        form.instance.university = university
        form.instance.user = self.request.user
        return super().form_valid(form)