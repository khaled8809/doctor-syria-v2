from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path(
        "articles/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("api/search/", views.search_view, name="search"),
    path("api/contact/", views.contact_form, name="contact_form"),
    path(
        "api/medical-locations/<int:area_id>/",
        views.get_medical_locations,
        name="medical_locations",
    ),
]
