from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.review.models import Review


class ReviewAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['job', 'user', 'rating']


admin.site.register(Review, ReviewAdmin)
