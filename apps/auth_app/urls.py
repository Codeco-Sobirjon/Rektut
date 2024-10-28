from django.urls import path

from apps.auth_app.api.views import views
from apps.auth_app.api.views import oauth2

from apps.auth_app.api.views.oauth2 import GoogleModelViewSet


urlpatterns = [
    path('register/', views.RegisterViews.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profile/', views.ProfileViews.as_view()),
    path('reset_password/', views.ResetPasswordView.as_view()),
    path("social-media/", GoogleModelViewSet.as_view({"post": "social_media_auth"}), name="social_media_auth"),
]