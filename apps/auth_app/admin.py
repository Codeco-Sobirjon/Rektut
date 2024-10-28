from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from apps.auth_app.models import (
    SocialMedia,
    SocialThrough,
    CustomUser
)


class SocialThroughInline(admin.TabularInline):
    model = SocialThrough
    extra = 1


class NewUser(ImportExportModelAdmin, UserAdmin):
    model = CustomUser
    list_display = ['email', 'phone', 'is_active', 'is_staff', ]
    search_fields = ['email', 'phone', 'groups']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Personal Information',
         {'fields': ('is_agree_terms', 'photo', 'about', 'update_about', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    inlines = [SocialThroughInline, ]


class SocialMediaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title', 'icon', 'date_create']


class SocialThroughAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'user', 'social', 'url', 'date_update', 'date_create']


admin.site.register(CustomUser, NewUser)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(SocialThrough, SocialThroughAdmin)
