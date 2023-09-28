from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from unidecode import unidecode

class University(models.Model):
    name = models.CharField(max_length=150)
    search_name = models.CharField(max_length=150, blank=True)
    voivodeship = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    link = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return f"{self.name}"

class Review(models.Model):
    title = models.CharField( max_length=150)
    description = models.CharField( max_length=3000)
    rating = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    add_date = models.DateTimeField(default=timezone.now, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the review is an existing instance (not a new one)
            previous_review = Review.objects.get(pk=self.pk)
            if self.title != previous_review.title or self.description != previous_review.description:
                # Create a new ReviewHistory entry
                ReviewHistory.objects.create(
                    review=previous_review,
                    title=previous_review.title,
                    description=previous_review.description,
                    rating=previous_review.rating,
                    modified_by=self.user,  # Assuming you have a User reference in the Review model
                )
        super(Review, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Create a ReviewHistory entry before deleting the review
        ReviewHistory.objects.create(
            review=self,
            title=self.title,
            description=self.description,
            rating=self.rating,
            modified_by=self.user,  # Assuming you have a User reference in the Review model
        )
        self.active = False
        self.save()

class ReviewHistory(models.Model):
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=3000)
    rating = models.IntegerField()
    modified_date = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"History for Review: {self.review.title} ({self.modified_date})"

class Comment(models.Model):
    description = models.CharField( max_length=3000)
    add_date = models.DateTimeField(default=timezone.now, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        
    def __str__(self):
        return f"{self.description}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the comment is an existing instance (not a new one)
            previous_comment = Comment.objects.get(pk=self.pk)
            if self.description != previous_comment.description:
                # Create a new CommentHistory entry
                CommentHistory.objects.create(
                    comment=previous_comment,
                    description=previous_comment.description,
                    modified_by=self.user,  # Assuming you have a User reference in the Comment model
                )
        super(Comment, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Create a CommentHistory entry before deleting the comment
        CommentHistory.objects.create(
            comment=self,
            description=self.description,
            modified_by=self.user,  # Assuming you have a User reference in the Comment model
        )
        self.active = False
        self.save()

class CommentHistory(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=3000)
    modified_date = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"History for Comment: {self.comment.description} ({self.modified_date})"

class ReviewReport(models.Model):
    description = models.CharField( max_length=3000)  
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'ReviewReport'
        verbose_name_plural = 'ReviewReports'

    def __str__(self):
        return f"{self.description}"

class CommentReport(models.Model):
    description = models.CharField( max_length=3000)  
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'CommentReport'
        verbose_name_plural = 'CommentReports'

    def __str__(self):
        return f"{self.description}"     
    
