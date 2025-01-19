from django.urls import path
from rest_framework import routers

from . import views

app_name = "medical_education"

# API Router
router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'simulations', views.VirtualSimulationViewSet)
router.register(r'resources', views.EducationalResourceViewSet)
router.register(r'assessments', views.AssessmentViewSet)

urlpatterns = [
    # Courses
    path("courses/", views.CourseListView.as_view(), name="course-list"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("courses/create/", views.CourseCreateView.as_view(), name="course-create"),
    path("courses/<int:pk>/enroll/", views.CourseEnrollmentView.as_view(), name="course-enroll"),
    path("courses/<int:pk>/progress/", views.CourseProgressView.as_view(), name="course-progress"),
    path("courses/categories/", views.CourseCategoryView.as_view(), name="course-categories"),
    
    # Virtual Simulations
    path("simulations/", views.VirtualSimulationListView.as_view(), name="simulation-list"),
    path("simulations/<int:pk>/", views.VirtualSimulationDetailView.as_view(), name="simulation-detail"),
    path("simulations/practice/", views.SimulationPracticeView.as_view(), name="simulation-practice"),
    path("simulations/scenarios/", views.SimulationScenarioView.as_view(), name="simulation-scenarios"),
    
    # Medical Library
    path("library/", views.MedicalLibraryListView.as_view(), name="library-list"),
    path("library/search/", views.LibrarySearchView.as_view(), name="library-search"),
    path("library/categories/", views.LibraryCategoryView.as_view(), name="library-categories"),
    path("library/favorites/", views.LibraryFavoritesView.as_view(), name="library-favorites"),
    
    # Educational Resources
    path("resources/", views.EducationalResourceView.as_view(), name="resources"),
    path("resources/videos/", views.VideoResourceView.as_view(), name="video-resources"),
    path("resources/documents/", views.DocumentResourceView.as_view(), name="document-resources"),
    path("resources/presentations/", views.PresentationResourceView.as_view(), name="presentation-resources"),
    
    # Assessments and Quizzes
    path("assessments/", views.AssessmentListView.as_view(), name="assessment-list"),
    path("assessments/<int:pk>/", views.AssessmentDetailView.as_view(), name="assessment-detail"),
    path("assessments/create/", views.AssessmentCreateView.as_view(), name="assessment-create"),
    path("assessments/results/", views.AssessmentResultView.as_view(), name="assessment-results"),
    
    # CME (Continuing Medical Education)
    path("cme/", views.CMEDashboardView.as_view(), name="cme-dashboard"),
    path("cme/credits/", views.CMECreditsView.as_view(), name="cme-credits"),
    path("cme/certificates/", views.CMECertificateView.as_view(), name="cme-certificates"),
    
    # Discussion Forums
    path("forums/", views.DiscussionForumView.as_view(), name="forums"),
    path("forums/topics/", views.ForumTopicView.as_view(), name="forum-topics"),
    path("forums/posts/", views.ForumPostView.as_view(), name="forum-posts"),
    
    # Progress Tracking
    path("progress/", views.LearningProgressView.as_view(), name="learning-progress"),
    path("progress/analytics/", views.ProgressAnalyticsView.as_view(), name="progress-analytics"),
    path("progress/reports/", views.ProgressReportView.as_view(), name="progress-reports"),
    
    # Settings
    path("settings/", views.EducationSettingsView.as_view(), name="education-settings"),
    path("settings/notifications/", views.NotificationSettingsView.as_view(), name="notification-settings"),
    path("settings/preferences/", views.LearningPreferencesView.as_view(), name="learning-preferences"),
]

urlpatterns += router.urls
