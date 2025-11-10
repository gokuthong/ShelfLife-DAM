from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AssetViewSet, basename='asset')
router.register(r'metadata', views.MetadataViewSet, basename='metadata')

urlpatterns = [
    path('search/', views.search_assets, name='search_assets'),
    path('', include(router.urls)),
]
