from django.contrib import admin

from .models import ReviewReport, University, Review

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'voivodeship')
    list_filter = ('name', 'city', 'voivodeship')

    def __str__(self):
        return self.name

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'rating', 'university', 'user')
    list_filter = ('rating', 'university', 'user')  

class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('description',)
    list_filter = ('review',) 

admin.site.register(University, UniversityAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewReport, ReviewReportAdmin)