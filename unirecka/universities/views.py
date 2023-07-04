from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.db.models import Avg
from .models import Review, ReviewReport, University
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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
    
    universities = universities.annotate(avg_rating=Avg('review__rating'))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        university = self.get_object()
        reviews = university.review_set.all().order_by('-add_date')
        context['reviews'] = reviews
        return context


class ReviewCreateView(CreateView):
    model = Review
    template_name = 'universities/review_create.html'
    fields = ['title', 'description', 'rating']
    success_url = reverse_lazy('university_list')

    def form_valid(self, form):
        university = get_object_or_404(University, id=self.kwargs['university_id'])
        form.instance.university = university
        form.instance.user = self.request.user
        messages.success(self.request, 'Pomyślnie dodano opinię.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Wystąpił błąd podczas dodawania opinii. Sprawdź podane dane. Tytuł nie może być zbyt długi.')
        return super().form_invalid(form)
    

class ReviewReportCreateView(CreateView):
    model = ReviewReport
    template_name = 'universities/reviewreport_create.html'
    fields = ['description']
    success_url = reverse_lazy('university_list')

    def form_valid(self, form):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        form.instance.review = review
        messages.success(self.request, 'Pomyślnie zgłoszono opinię. Zgłoszenie zostanie sprawdzone jak najszybciej')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Wystąpił błąd podczas zgłaszania opinii. Sprawdź podane dane. Opis nie może być zbyt długi.')
        return super().form_invalid(form)
    
@login_required
@require_POST
def review_like(request):
    review_id = request.POST.get('id')
    action = request.POST.get('action')
    print(review_id)
    if review_id and action:
        try:
            review = Review.objects.get(id=review_id)
            if action == 'like':
                review.users_like.add(request.user)
            else:
                review.users_like.remove(request.user)
            return JsonResponse({
                'status':'ok'
            })
        except:
            pass
    return JsonResponse({
                'status':'ok'
            })