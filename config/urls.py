from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("careerforge-admin-Charan9494/", admin.site.urls),
    path('', include('jobs.urls')),
    path('', include('resumes.urls')),
    path('', include('accounts.urls')),
    path('', include('applications.urls')),
    path(
    "",
    include("ai_agents.urls")
),
    path(
    '',
    include(
        'analytics.urls'
    )
),
    path(
    "",
    include("notifications.urls")
),
    path(

'accounts/',

include('allauth.urls')

),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
