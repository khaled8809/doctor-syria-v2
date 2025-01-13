from django.urls import path

from . import views

app_name = "laboratory"

urlpatterns = [
    path("tests/", views.LabTestListCreateView.as_view(), name="test-list-create"),
    path("tests/<int:pk>/", views.LabTestDetailView.as_view(), name="test-detail"),
    path(
        "test-requests/",
        views.TestRequestListCreateView.as_view(),
        name="test-request-list-create",
    ),
    path(
        "test-requests/<int:pk>/",
        views.TestRequestDetailView.as_view(),
        name="test-request-detail",
    ),
    path(
        "test-results/",
        views.TestResultListCreateView.as_view(),
        name="test-result-list-create",
    ),
    path(
        "test-results/<int:pk>/",
        views.TestResultDetailView.as_view(),
        name="test-result-detail",
    ),
    path(
        "sample-collections/",
        views.SampleCollectionListCreateView.as_view(),
        name="sample-collection-list-create",
    ),
    path(
        "sample-collections/<int:pk>/",
        views.SampleCollectionDetailView.as_view(),
        name="sample-collection-detail",
    ),
]
