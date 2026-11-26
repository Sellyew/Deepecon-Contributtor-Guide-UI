from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path("papers/<slug:paper_id>/guidance/", views.guidance, name="guidance"),
    path("papers/<slug:paper_id>/submit/", views.submit, name="submit"),
    path("papers/<slug:paper_id>/submit/uploads/start/", views.upload_start, name="upload_start"),
    path("papers/<slug:paper_id>/submit/uploads/plain/", views.upload_plain, name="upload_plain"),
    path("papers/<slug:paper_id>/submit/uploads/<str:upload_id>/", views.upload_status, name="upload_status"),
    path("papers/<slug:paper_id>/submit/uploads/<str:upload_id>/chunk/", views.upload_chunk, name="upload_chunk"),
    path("papers/<slug:paper_id>/submit/uploads/<str:upload_id>/remove/", views.upload_remove, name="upload_remove"),
]
