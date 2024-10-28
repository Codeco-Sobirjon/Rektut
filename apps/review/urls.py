from django.urls import path
from apps.review.api.views import views

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='review-get-post'),
    path('/<int:pk>/', views.ReviewDetailsViews.as_view(), name='review-get-put-delete')
]