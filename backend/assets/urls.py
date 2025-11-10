from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet, basename='asset')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.search_assets, name='search-assets'),
    path('search/suggestions/', views.search_suggestions, name='search-suggestions'),
]
