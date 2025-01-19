from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AnswerForm, CommentForm, QuestionForm
from .models import Answer, Category, Comment, Question, QuestionBookmark


class CategoryListView(ListView):
    model = Category
    template_name = "qa/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context["categories"]:
            category.questions_count = Question.objects.filter(
                category=category, status="published"
            ).count()
        return context


class QuestionListView(ListView):
    model = Question
    template_name = "qa/question_list.html"
    context_object_name = "questions"
    paginate_by = 20

    def get_queryset(self):
        queryset = Question.objects.filter(status="published")

        # فلترة حسب التصنيف
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # فلترة حسب البحث
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__icontains=query)
            )

        # فلترة حسب الترتيب
        sort = self.request.GET.get("sort", "-created_at")
        if sort == "popular":
            queryset = queryset.annotate(answers_count=Count("answer")).order_by(
                "-answers_count"
            )
        elif sort == "views":
            queryset = queryset.order_by("-views_count")
        else:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = self.kwargs.get("category_slug")
        context["current_sort"] = self.request.GET.get("sort", "-created_at")
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = "qa/question_detail.html"
    context_object_name = "question"

    def get_object(self):
        obj = super().get_object()
        if not self.request.session.get(f"question_viewed_{obj.id}"):
            obj.views_count += 1
            obj.save()
            self.request.session[f"question_viewed_{obj.id}"] = True
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.object.answer_set.all()
        if self.request.user.is_authenticated:
            context["is_bookmarked"] = QuestionBookmark.objects.filter(
                question=self.object, user=self.request.user
            ).exists()
        return context


@method_decorator(login_required, name="dispatch")
class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    success_url = reverse_lazy("qa:question_list")

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient_profile
        messages.success(self.request, "تم نشر سؤالك بنجاح وسيتم مراجعته")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "qa/question_form.html"

    def get_queryset(self):
        return Question.objects.filter(patient__user=self.request.user)


@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.doctor = request.user.doctor_profile
            answer.save()
            messages.success(request, "تمت إضافة إجابتك بنجاح")
            return redirect("qa:question_detail", slug=question.slug)
    else:
        form = AnswerForm()

    return render(request, "qa/answer_form.html", {"form": form, "question": question})


@login_required
def vote_answer(request, answer_id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, id=answer_id)
        user = request.user

        if user in answer.upvotes.all():
            answer.upvotes.remove(user)
            action = "removed"
        else:
            answer.upvotes.add(user)
            action = "added"

        return JsonResponse(
            {
                "status": "success",
                "action": action,
                "upvotes_count": answer.upvotes_count,
            }
        )

    return JsonResponse({"status": "error"}, status=400)


@login_required
def mark_best_answer(request, answer_id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, id=answer_id)

        # تأكد من أن المستخدم هو صاحب السؤال
        if request.user != answer.question.patient.user:
            return JsonResponse(
                {"status": "error", "message": "غير مصرح لك بهذا الإجراء"}, status=403
            )

        # إزالة علامة أفضل إجابة من الإجابات الأخرى
        answer.question.answer_set.filter(is_best=True).update(is_best=False)

        # تعيين هذه الإجابة كأفضل إجابة
        answer.is_best = True
        answer.save()

        return JsonResponse(
            {"status": "success", "message": "تم تحديد الإجابة كأفضل إجابة"}
        )

    return JsonResponse({"status": "error"}, status=400)


@login_required
def toggle_bookmark(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Question, id=question_id)
        bookmark, created = QuestionBookmark.objects.get_or_create(
            question=question, user=request.user
        )

        if not created:
            bookmark.delete()
            action = "removed"
        else:
            action = "added"

        return JsonResponse({"status": "success", "action": action})

    return JsonResponse({"status": "error"}, status=400)


@login_required
def add_comment(request, answer_id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, id=answer_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = answer
            comment.user = request.user
            comment.save()

            return JsonResponse(
                {
                    "status": "success",
                    "comment": {
                        "id": comment.id,
                        "content": comment.content,
                        "user_name": comment.user.get_full_name(),
                        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    },
                }
            )

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    return JsonResponse({"status": "error"}, status=400)
