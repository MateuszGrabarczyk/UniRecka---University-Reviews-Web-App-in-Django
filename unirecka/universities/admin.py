from django.contrib import admin

from .models import Comment, CommentHistory, CommentReport, ReviewHistory, ReviewReport, University, Review
from unidecode import unidecode

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'voivodeship')
    list_filter = ('name', 'city', 'voivodeship')
    actions = ['save_all_universities']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'rating', 'university', 'user', 'active')
    list_filter = ('rating', 'university', 'user', 'active')  

class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('description', 'active')
    list_filter = ('review', 'active')

    def __str__(self):
        return self.description
    
class ReviewHistoryAdmin(admin.ModelAdmin):
    list_display = ('review', 'title', 'description', 'modified_date', 'modified_by')
    list_filter = ('review__university', 'modified_date', 'modified_by')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'active', )
    list_filter = ('review','user', 'active')

    def __str__(self):
        return self.description
    
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ('description', 'active')
    list_filter = ('comment', 'active')

    def __str__(self):
        return self.description
    
class CommentHistoryAdmin(admin.ModelAdmin):
    list_display = ('comment', 'description', 'modified_date', 'modified_by')
    list_filter = ('comment__review', 'modified_date', 'modified_by')

admin.site.register(University, UniversityAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewReport, ReviewReportAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
admin.site.register(CommentHistory, CommentHistoryAdmin)
admin.site.register(ReviewHistory, ReviewHistoryAdmin)

