from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from unidecode import unidecode

from .models import Comment, CommentReport, Review, ReviewReport, University
from .utils import check_if_has_cursed_words


def university_list(request):
    name = request.GET.get("name", "")
    city = request.GET.get("city", "")
    voivodeship = request.GET.get("voivodeship", "")
    universities = University.objects.all()
    city_and_voivodeship = {}

    for uni in universities:
        city_and_voivodeship[uni.city] = uni.voivodeship

    cities = universities.values_list("city", flat=True).distinct()
    voivodeships = universities.values_list("voivodeship", flat=True).distinct()
    if name != "":
        universities = universities.filter(search_name__icontains=unidecode(name))
    if city != "":
        if voivodeship == "":
            universities = universities.filter(city=city)
        elif voivodeship != city_and_voivodeship[city]:
            messages.warning(
                request,
                f"Wybrano województwo, w którym nie znajduje się miasto {city}. Domyślnie wybrano województwo {city_and_voivodeship[city].capitalize()}.",
            )
            universities = universities.filter(
                voivodeship=city_and_voivodeship[city], city=city
            )
            voivodeship = city_and_voivodeship[city]
            universities = universities.annotate(
                avg_rating=Avg("review__rating", filter=Q(review__active=True))
            )
            for university in universities:
                print(
                    f"University: {university.name}, Average Rating: {university.avg_rating}"
                )

            return render(
                request,
                "universities/university_list.html",
                {
                    "universities": universities,
                    "name_value": name,
                    "city_value": city,
                    "voivodeship_value": voivodeship,
                    "cities": sorted(cities),
                    "voivodeships": sorted(voivodeships),
                },
            )

        universities = universities.filter(
            voivodeship=city_and_voivodeship[city], city=city
        )
        universities = universities.annotate(
            avg_rating=Avg("review__rating", filter=Q(review__active=True))
        )

        return render(
            request,
            "universities/university_list.html",
            {
                "universities": universities,
                "name_value": name,
                "city_value": city,
                "voivodeship_value": voivodeship,
                "cities": sorted(cities),
                "voivodeships": sorted(voivodeships),
            },
        )

    if voivodeship != "":
        if city == "":
            universities = universities.filter(voivodeship=voivodeship)

    universities = universities.annotate(
        avg_rating=Avg("review__rating", filter=Q(review__active=True))
    )

    return render(
        request,
        "universities/university_list.html",
        {
            "universities": universities,
            "name_value": name,
            "city_value": city,
            "voivodeship_value": voivodeship,
            "cities": sorted(cities),
            "voivodeships": sorted(voivodeships),
        },
    )


class UniversityDetailView(DetailView):
    model = University
    template_name = "universities/university_detail.html"
    context_object_name = "university"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        university = self.get_object()

        sort_method = self.request.GET.get("sort_method", "newest")
        start_date = self.request.GET.get("start_date", "")
        end_date = self.request.GET.get("end_date", "")

        allowed_sort_methods = [
            "newest",
            "oldest",
            "most_comments",
            "most_likes",
            "best_ratings",
            "worst_ratings",
        ]
        if sort_method not in allowed_sort_methods:
            raise Http404("Invalid sort method")

        if sort_method == "newest":
            reviews = university.review_set.all().order_by("-add_date")
        elif sort_method == "oldest":
            reviews = university.review_set.all().order_by("add_date")
        elif sort_method == "most_comments":
            reviews = university.review_set.annotate(
                num_comments=Count("comment")
            ).order_by("-num_comments", "-add_date")
        elif sort_method == "most_likes":
            reviews = university.review_set.annotate(
                num_likes=Count("users_like")
            ).order_by("-num_likes", "-add_date")
        elif sort_method == "best_ratings":
            reviews = university.review_set.all().order_by("-rating")
        elif sort_method == "worst_ratings":
            reviews = university.review_set.all().order_by("rating")

        context["has_reviews"] = bool(reviews.filter(active=True))

        if start_date and end_date:
            if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(
                end_date, "%Y-%m-%d"
            ):
                temp = start_date
                start_date = end_date
                end_date = temp
                messages.info(
                    self.request,
                    "Pierwsza data jest większa od drugiej, dlatego poprawiono kolejność.",
                )

        if start_date:
            reviews = reviews.filter(
                add_date__gte=datetime.combine(
                    datetime.strptime(start_date, "%Y-%m-%d").date(), time.min
                )
            )

        if end_date:
            reviews = reviews.filter(
                add_date__lte=datetime.combine(
                    datetime.strptime(end_date, "%Y-%m-%d").date(), time.max
                )
            )

        reviews = reviews.annotate(
            num_active_comments=Count("comment", filter=Q(comment__active=True))
        )

        context["sort_method"] = sort_method
        context["reviews"] = reviews.filter(active=True)

        context["oldest_review_date"] = start_date if start_date else ""
        context["newest_review_date"] = end_date if end_date else ""

        return context


class ReviewCreateView(CreateView):
    model = Review
    template_name = "universities/review_create.html"
    fields = ["title", "description", "rating"]

    def get_success_url(self):
        return reverse_lazy(
            "university_detail", kwargs={"pk": self.kwargs["university_id"]}
        )

    def form_valid(self, form):
        university = get_object_or_404(University, id=self.kwargs["university_id"])
        form.instance.university = university
        form.instance.user = self.request.user

        description = form.cleaned_data.get("description", "")
        title = form.cleaned_data.get("title", "")

        if check_if_has_cursed_words(title.split()):
            messages.error(
                self.request, "Twój tytuł zawiera niedozwolone słowo, spróbuj ponownie."
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "review_create",
                    kwargs={"university_id": self.kwargs["university_id"]},
                )
            )

        if check_if_has_cursed_words(description.split()):
            messages.error(
                self.request, "Twój opis zawiera niedozwolone słowo, spróbuj ponownie."
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "review_create",
                    kwargs={"university_id": self.kwargs["university_id"]},
                )
            )

        messages.success(self.request, "Pomyślnie dodano recenzję.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Wystąpił błąd podczas dodawania opinii. Sprawdź podane dane. Tytuł nie może być zbyt długi.",
        )
        return super().form_invalid(form)


class ReviewUpdateView(UpdateView):
    model = Review
    template_name = "universities/review_update.html"
    fields = ["title", "description", "rating"]

    def form_valid(self, form):
        description = form.cleaned_data.get("description", "")
        title = form.cleaned_data.get("title", "")

        if check_if_has_cursed_words(title.split()):
            messages.error(
                self.request, "Twój tytuł zawiera niedozwolone słowo, spróbuj ponownie."
            )
            return HttpResponseRedirect(
                reverse_lazy("review_update", kwargs={"pk": self.object.id})
            )

        if check_if_has_cursed_words(description.split()):
            messages.error(
                self.request, "Twój opis zawiera niedozwolone słowo, spróbuj ponownie."
            )
            return HttpResponseRedirect(
                reverse_lazy("review_update", kwargs={"pk": self.object.id})
            )
        messages.success(self.request, "Pomyślnie edytowano recenzję.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Wystąpił błąd podczas edytowania opinii. Sprawdź podane dane. Tytuł nie może być zbyt długi.",
        )
        return super().form_invalid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"user_id": self.request.user.id})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "universities/review_delete.html"

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"user_id": self.request.user.id})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie usunięto recenzję.")
        return super().form_valid(form)


class ReviewDetailView(DetailView):
    model = Review
    template_name = "universities/review_detail.html"
    context_object_name = "review"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        comments = review.comment_set.filter(active=True).order_by("add_date")
        context["comments"] = comments
        return context


class CommentCreateView(CreateView):
    model = Comment
    template_name = "universities/comment_create.html"
    fields = ["description"]

    def get_success_url(self):
        return reverse_lazy("review_detail", kwargs={"pk": self.kwargs["review_id"]})

    def form_valid(self, form):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        form.instance.review = review
        form.instance.user = self.request.user

        description = form.cleaned_data.get("description", "")

        if check_if_has_cursed_words(description.split()):
            messages.error(
                self.request,
                "Twój komentarz zawiera niedozwolone słowo, spróbuj ponownie.",
            )
            return HttpResponseRedirect(
                reverse("comment_create", kwargs={"review_id": review.id})
            )

        messages.success(self.request, "Pomyślnie dodano komentarz")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Wystąpił błąd podczas dodawania komentarza. Opis może być za długi.",
        )
        return super().form_invalid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = "universities/comment_update.html"
    fields = ["description"]

    def form_valid(self, form):
        description = form.cleaned_data.get("description", "")

        if check_if_has_cursed_words(description.split()):
            messages.error(
                self.request,
                "Twój komentarz zawiera niedozwolone słowo, spróbuj ponownie.",
            )
            return HttpResponseRedirect(
                reverse("comment_update", kwargs={"pk": self.object.id})
            )
        messages.success(self.request, "Pomyślnie edytowano komentarz.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Wystąpił błąd podczas edytowania komentarza. Sprawdź podane dane. Opis nie może być zbyt długi.",
        )
        return super().form_invalid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"user_id": self.request.user.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "universities/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"user_id": self.request.user.id})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie usunięto komentarz.")
        return super().form_valid(form)


class ReviewReportCreateView(CreateView):
    model = ReviewReport
    template_name = "universities/reviewreport_create.html"
    fields = ["description"]
    success_url = reverse_lazy("university_list")

    def form_valid(self, form):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        form.instance.review = review
        messages.success(
            self.request,
            "Pomyślnie zgłoszono recenzję. Zgłoszenie zostanie sprawdzone jak najszybciej",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Wystąpił błąd podczas zgłaszania formularza. Sprawdź podane dane. Opis nie może być zbyt długi.",
        )
        return super().form_invalid(form)


class CommentReportCreateView(CreateView):
    model = CommentReport
    template_name = "universities/commentreport_create.html"
    fields = ["description"]

    def get_success_url(self):
        return reverse_lazy("review_detail", kwargs={"pk": self.kwargs["review_id"]})

    def form_valid(self, form):
        comment = get_object_or_404(Comment, id=self.kwargs["comment_id"])
        form.instance.comment = comment
        messages.success(
            self.request,
            "Pomyślnie zgłoszono komentarz. Zgłoszenie zostanie sprawdzone jak najszybciej",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Wystąpił błąd podczas zgłaszania formularza. Sprawdź podane dane. Opis nie może być zbyt długi.",
        )
        return super().form_invalid(form)


@login_required
@require_POST
def review_like(request):
    review_id = request.POST.get("id")
    action = request.POST.get("action")
    if review_id and action:
        try:
            review = Review.objects.get(id=review_id)
            if action == "like":
                review.users_like.add(request.user)
            else:
                review.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Review.DoesNotExist:
            pass
    return JsonResponse({"status": "ok"})
