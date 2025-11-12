from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
<<<<<<< HEAD
        title="ShelfLife DAM API",
        default_version='v1',
        description="Digital Asset Management System API",
        terms_of_service="https://www.example.com/terms/",
=======
        title="ShelfLifeDAM API",
        default_version='v1',
        description="Digital Asset Management System API",
        terms_of_service="https://www.shelflifedam.com/terms/",
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
        contact=openapi.Contact(email="contact@shelflifedam.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('api/auth/', include('users.urls')),
    path('api/assets/', include('assets.urls')),

    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
=======

    # API URLs
    path('api/auth/', include('users.urls')),
    path('api/assets/', include('assets.urls')),
    path('api/activity/', include('activity.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
<<<<<<< HEAD
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
