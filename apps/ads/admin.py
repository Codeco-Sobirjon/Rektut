from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from apps.ads.models import *


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'icon', 'date_create']
    search_fields = ['name', 'subcategory']


class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'short_name', 'date_create']
    search_fields = ['name', 'short_name']


class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'country', 'short_name', 'date_create']
    search_fields = ['name', 'country']


class OptionalFieldAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'key', 'type', 'is_required', 'default', 'max_length', 'min_length', 'is_active']


class OptionalFieldThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['job', 'optional_field', 'value', 'image', 'file']


class JobAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'category', 'city', 'contact_number', 'email', 'name', 'user']
    search_fields = ['title', 'user', 'category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(OptionalField, OptionalFieldAdmin)
admin.site.register(OptionalFieldThrough, OptionalFieldThroughAdmin)
admin.site.register(Job, JobAdmin)



