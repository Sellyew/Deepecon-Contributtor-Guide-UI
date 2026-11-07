from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "DeepEcon contributor site: team administration"
admin.site.site_title = "DeepEcon team administration"
admin.site.index_title = "Papers, contributors, and records"

urlpatterns = [
    path("team-admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("contributors.urls")),
]
