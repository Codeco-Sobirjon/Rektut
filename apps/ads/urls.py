from django.urls import path
from apps.ads.api.views import job_views
from apps.ads.api.views import views

urlpatterns = [
    path('', job_views.JobListView.as_view()),
    path('create/', job_views.AdsCreateView.as_view()),
    path('<int:pk>/', job_views.AdsDetailView.as_view()),
    path('optional/field/', views.OptionalFieldListView.as_view())
]