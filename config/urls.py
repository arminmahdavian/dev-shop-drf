"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

admin_urls = [
    path('api/admin/users/', include(('auths.users.urls.admin', 'auths.users'), namespace='users-admin')),
    path('api/admin/catalogue/', include(('catalogue.urls.admin', 'DevShop.apps.catalogue'), namespace='catalogue-admin')),
]

front_urls = [
    path('api/front/users/', include(('auths.users.urls.front', 'auths.users'), namespace='users-front')),
    path('api/front/catalogue/', include(('catalogue.urls.front', 'DevShop.apps.catalogue'), namespace='catalogue-front')),
]

doc_patterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),

] + admin_urls + front_urls + doc_patterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "DevShop"
admin.site.site_header = "DevShop"
admin.site.index_title = "DevShop"

