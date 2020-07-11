from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = "Адмнистрирование Nav Info"
admin.site.site_title = "Адмнистрирование Nav Info"
admin.site.index_title = "Nav Info"

schema_view = get_schema_view(
    openapi.Info(
        title="Nav Info API",
        default_version='v1',
        contact=openapi.Contact(email="beliy_ns@kuzro.ru"),
        license=openapi.License(name="MIT License"),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', schema_view.with_ui('swagger',
                                     cache_timeout=0), name='docs-ui'),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),
    path('api/', include('soap_client.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # Silk profiler
    urlpatterns = [
        path('silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns
