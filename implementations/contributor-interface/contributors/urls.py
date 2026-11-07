from django.urls import path

from . import views

app_name = "contributors"

urlpatterns = [
    path("", views.home, name="home"),
    path("i/<str:token>/", views.invitation_landing, name="invitation"),
    path("papers/<slug:paper_id>/notice/", views.notice, name="notice"),
    path("papers/<slug:paper_id>/", views.my_paper, name="my_paper"),
    path("papers/<slug:paper_id>/package/", views.package_download, name="package"),
]
