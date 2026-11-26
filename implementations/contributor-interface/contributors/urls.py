from django.urls import path

from . import selection_views as sv
from . import views

app_name = "contributors"

urlpatterns = [
    path("", views.home, name="home"),
    path("i/<str:token>/", views.invitation_landing, name="invitation"),
    path("papers/", views.papers, name="papers"),
    path("papers/<slug:paper_id>/choose/", views.choose, name="choose"),
    path("papers/<slug:paper_id>/notice/", views.notice, name="notice"),
    path("papers/<slug:paper_id>/", views.my_paper, name="my_paper"),
    path("papers/<slug:paper_id>/package/", views.package_download, name="package"),
    path("papers/<slug:paper_id>/review/", sv.review_start, name="review"),
    path("papers/<slug:paper_id>/review/<str:item_id>/", sv.review_item, name="review_item"),
    path("papers/<slug:paper_id>/matrix/", sv.review_matrix, name="review_matrix"),
    path("papers/<slug:paper_id>/propose/", sv.propose, name="propose"),
    path("papers/<slug:paper_id>/propose/<str:proposal_id>/", sv.propose, name="proposal_edit"),
    path("papers/<slug:paper_id>/ask/", sv.ask, name="ask"),
    path("papers/<slug:paper_id>/confirm/", sv.confirm, name="confirm"),
    path("papers/<slug:paper_id>/my-review/", sv.my_review_download, name="my_review"),
]
