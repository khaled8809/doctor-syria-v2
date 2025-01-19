from django.urls import path

from . import views

app_name = "qa"

urlpatterns = [
    # صفحات التصنيفات
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    # صفحات الأسئلة
    path("", views.QuestionListView.as_view(), name="question_list"),
    path(
        "category/<slug:category_slug>/",
        views.QuestionListView.as_view(),
        name="category_questions",
    ),
    path(
        "question/<slug:slug>/",
        views.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    path("ask/", views.QuestionCreateView.as_view(), name="ask_question"),
    path(
        "question/<slug:slug>/edit/",
        views.QuestionUpdateView.as_view(),
        name="edit_question",
    ),
    # إضافة وتعديل الإجابات
    path("question/<int:question_id>/answer/", views.add_answer, name="add_answer"),
    path("answer/<int:answer_id>/vote/", views.vote_answer, name="vote_answer"),
    path(
        "answer/<int:answer_id>/best/", views.mark_best_answer, name="mark_best_answer"
    ),
    # التعليقات
    path("answer/<int:answer_id>/comment/", views.add_comment, name="add_comment"),
    # المفضلة
    path(
        "question/<int:question_id>/bookmark/",
        views.toggle_bookmark,
        name="toggle_bookmark",
    ),
]
