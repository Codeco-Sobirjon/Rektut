from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.team.models import *


class TeamRoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name']


class TeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'role']


admin.site.register(TeamRole, TeamRoleAdmin)
admin.site.register(Team, TeamAdmin)
