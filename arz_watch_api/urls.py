import os
from dotenv import load_dotenv
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static

# Loads the variables from the .env file into the environment
load_dotenv()

router = routers.DefaultRouter()

base_url: str = os.getenv("BASE_URL", "")

urlpatterns = [
    path(base_url, include(router.urls)),
    path(
        os.getenv("ADMIN_URL", "admin/"), admin.site.urls
    ),  # Admin URL without base_url
    path("scrapers/", include("scrapers.urls")),
    path("telegram/", include("telegram.urls")),
]

# Only add base_url once at the root level
urlpatterns = [path(base_url, include(urlpatterns))]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = "Arz Watch API Admin"
admin.site.site_header = "Arz Watch API Admin"
admin.site.site_title = "Arz Watch API"
