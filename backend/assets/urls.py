<<<<<<< HEAD
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
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet, basename='asset')
router.register(r'metadata', views.MetadataViewSet, basename='metadata')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_asset, name='upload_asset'),
    path('search/', views.search_assets, name='search_assets'),
]
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
