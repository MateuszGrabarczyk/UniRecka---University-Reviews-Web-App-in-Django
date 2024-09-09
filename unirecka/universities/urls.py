from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.university_list, name="university_list"),
    path("<int:pk>/", views.UniversityDetailView.as_view(), name="university_detail"),
    path("review/<int:pk>/", views.ReviewDetailView.as_view(), name="review_detail"),
    path(
        "review/history/<int:pk>/",
        login_required(views.ReviewHistoryListView.as_view()),
        name="review_history",
    ),
    path(
        "review/create/<int:university_id>/",
        login_required(views.ReviewCreateView.as_view()),
        name="review_create",
    ),
    path(
        "review/delete/<int:pk>/",
        login_required(views.ReviewDeleteView.as_view()),
        name="review_delete",
    ),
    path(
        "review/edit/<int:pk>/",
        login_required(views.ReviewUpdateView.as_view()),
        name="review_update",
    ),
    path(
        "review/report/<int:review_id>/",
        views.ReviewReportCreateView.as_view(),
        name="review_report_create",
    ),
    path("review/like", views.review_like, name="like"),
    path(
        "review/create/comment/<int:review_id>/",
        login_required(views.CommentCreateView.as_view()),
        name="comment_create",
    ),
    path(
        "review/edit/comment/<int:pk>/",
        login_required(views.CommentUpdateView.as_view()),
        name="comment_update",
    ),
    path(
        "review/comment/history/<int:pk>/",
        login_required(views.CommentHistoryListView.as_view()),
        name="comment_history",
    ),
    path(
        "review/delete/comment/<int:pk>/",
        login_required(views.CommentDeleteView.as_view()),
        name="comment_delete",
    ),
    path(
        "review/report/<int:review_id>/comment/<int:comment_id>/",
        views.CommentReportCreateView.as_view(),
        name="comment_report_create",
    ),
]
