from django.urls import path

from . import views

app_name = "laboratory"

urlpatterns = [
    # Lab Test URLs
    path("tests/", views.LabTestListView.as_view(), name="test-list"),
    path("tests/create/", views.LabTestCreateView.as_view(), name="test-create"),
    path("tests/<int:pk>/", views.LabTestDetailView.as_view(), name="test-detail"),
    path(
        "tests/<int:pk>/update/", views.LabTestUpdateView.as_view(), name="test-update"
    ),
    path(
        "tests/<int:pk>/delete/", views.LabTestDeleteView.as_view(), name="test-delete"
    ),
    # Lab Result URLs
    path("results/", views.LabResultListView.as_view(), name="result-list"),
    path("results/create/", views.LabResultCreateView.as_view(), name="result-create"),
    path(
        "results/<int:pk>/", views.LabResultDetailView.as_view(), name="result-detail"
    ),
    path(
        "results/<int:pk>/update/",
        views.LabResultUpdateView.as_view(),
        name="result-update",
    ),
    path(
        "results/<int:pk>/delete/",
        views.LabResultDeleteView.as_view(),
        name="result-delete",
    ),
]
