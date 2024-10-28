from django.urls import path
from apps.team.api.views import views


urlpatterns = [
    path('', views.TeamListViews.as_view(), name='team_get_post'),
    path('<int:pk>/', views.TeamDetailsViews.as_view(), name='team_get_put_delete'),
    path('roles/', views.TeamRoleListViews.as_view(), name='team_role_get_post'),
    path('role/<int:pk>/', views.TeamRoleListViews.as_view(), name="team_role_get_update_delete"),
]