from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from apps.ads.api.views import views
from rest_framework_simplejwt import views as jwt_views

from apps.ads.api.views.job_views import MyAdsListViews

admin.site.site_url = None
schema_view = get_schema_view(
    openapi.Info(
        title="ADS Backend",
        default_version="v1",
        description="ADS Backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/', include('apps.auth_app.urls')),
    path('ads/', include('apps.ads.urls')),
    path('review/', include('apps.review.urls')),
    path('team/', include('apps.team.urls')),
    path('myads/', MyAdsListViews.as_view()),

    # category
    path('categories/', views.CategoryListView.as_view()),
    path('category/<int:pk>/', views.CategoryDetailView.as_view()),

    # country
    path('countries/', views.CountryListView.as_view()),
    path('county/<int:pk>/', views.CountryDetailView.as_view()),

    # city
    path('cities/', views.CityListView.as_view()),
    path('city/<int:pk>/', views.CityDetailViews.as_view())
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]