from django.urls import path
from . import views

urlpatterns = [
    path('', views.university_list, name='university_list'),
    path('<int:pk>/', views.UniversityDetailView.as_view(), name='university_detail'),
    path('review/create/<int:university_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/report/<int:review_id>/', views.ReviewReportCreateView.as_view(), name='review_report_create'),
]