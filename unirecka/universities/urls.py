from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.university_list, name='university_list'),
    path('<int:pk>/', views.UniversityDetailView.as_view(), name='university_detail'),
    path('review/create/<int:university_id>/', login_required(views.ReviewCreateView.as_view()), name='review_create'),
    path('review/delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('review/report/<int:review_id>/', login_required(views.ReviewReportCreateView.as_view()), name='review_report_create'),
    path('review/like', views.review_like, name='like')
]