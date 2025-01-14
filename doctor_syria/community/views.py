from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, EventForm, GroupForm, HealthTipForm, PostForm, StoryForm
from .models import Comment, Event, Group, HealthTip, Notification, Post, Story


class GroupListView(ListView):
    model = Group
    template_name = "community/group_list.html"
    context_object_name = "groups"
    paginate_by = 12

    def get_queryset(self):
        queryset = Group.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


@method_decorator(login_required, name="dispatch")
class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "community/group_form.html"
    success_url = reverse_lazy("community:group_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)
        form.instance.moderators.add(self.request.user)
        messages.success(self.request, "تم إنشاء المجموعة بنجاح")
        return response


class GroupDetailView(DetailView):
    model = Group
    template_name = "community/group_detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(group=self.object)
        context["is_member"] = self.request.user in self.object.members.all()
        context["is_moderator"] = self.request.user in self.object.moderators.all()
        return context


@login_required
def join_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    if request.user not in group.members.all():
        group.members.add(request.user)
        messages.success(request, f"تم الانضمام إلى {group.name} بنجاح")
    return redirect("community:group_detail", slug=slug)


class EventListView(ListView):
    model = Event
    template_name = "community/event_list.html"
    context_object_name = "events"
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(end_date__gte=timezone.now()).order_by(
            "start_date"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["past_events"] = Event.objects.filter(
            end_date__lt=timezone.now()
        ).order_by("-end_date")[:5]
        return context


@method_decorator(login_required, name="dispatch")
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "community/event_form.html"
    success_url = reverse_lazy("community:event_list")

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "تم إنشاء الفعالية بنجاح")
        return response


@login_required
def register_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.user not in event.participants.all():
        if event.participants.count() < event.max_participants:
            event.participants.add(request.user)
            messages.success(request, f"تم التسجيل في {event.title} بنجاح")
        else:
            messages.error(request, "عذراً، الفعالية مكتملة العدد")
    return redirect("community:event_detail", slug=slug)


class HealthTipListView(ListView):
    model = HealthTip
    template_name = "community/health_tip_list.html"
    context_object_name = "tips"
    paginate_by = 10

    def get_queryset(self):
        queryset = HealthTip.objects.all()
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset


@method_decorator(login_required, name="dispatch")
class HealthTipCreateView(CreateView):
    model = HealthTip
    form_class = HealthTipForm
    template_name = "community/health_tip_form.html"
    success_url = reverse_lazy("community:health_tip_list")

    def form_valid(self, form):
        if hasattr(self.request.user, "doctor_profile"):
            form.instance.doctor = self.request.user.doctor_profile
            response = super().form_valid(form)
            messages.success(self.request, "تم نشر النصيحة الصحية بنجاح")
            return response
        else:
            messages.error(self.request, "عذراً، فقط الأطباء يمكنهم نشر النصائح الصحية")
            return redirect("community:health_tip_list")


class StoryListView(ListView):
    model = Story
    template_name = "community/story_list.html"
    context_object_name = "stories"
    paginate_by = 8

    def get_queryset(self):
        return Story.objects.filter(status="approved")


@method_decorator(login_required, name="dispatch")
class StoryCreateView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = "community/story_form.html"
    success_url = reverse_lazy("community:story_list")

    def form_valid(self, form):
        if hasattr(self.request.user, "patient_profile"):
            form.instance.patient = self.request.user.patient_profile
            response = super().form_valid(form)
            messages.success(self.request, "تم إرسال قصتك للمراجعة")
            return response
        else:
            messages.error(self.request, "عذراً، فقط المرضى يمكنهم مشاركة قصصهم")
            return redirect("community:story_list")


@login_required
def add_comment(request, content_type, object_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type_id = content_type
            comment.object_id = object_id
            comment.save()

            # إنشاء إشعار للمؤلف الأصلي
            content_object = comment.content_object
            if hasattr(content_object, "author"):
                recipient = content_object.author
            elif hasattr(content_object, "patient"):
                recipient = content_object.patient.user

            if recipient != request.user:
                Notification.objects.create(
                    recipient=recipient,
                    notification_type="comment",
                    title="تعليق جديد",
                    message=f"علق {request.user.get_full_name()} على {content_object}",
                    link=content_object.get_absolute_url(),
                )

            return JsonResponse(
                {
                    "status": "success",
                    "comment": {
                        "user": request.user.get_full_name(),
                        "content": comment.content,
                        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    },
                }
            )
    return JsonResponse({"status": "error"}, status=400)


@login_required
def toggle_like(request, content_type, object_id):
    if request.method == "POST":
        content_object = get_object_or_404(content_type.model_class(), id=object_id)
        if request.user in content_object.likes.all():
            content_object.likes.remove(request.user)
            action = "removed"
        else:
            content_object.likes.add(request.user)
            action = "added"

            # إنشاء إشعار
            if hasattr(content_object, "author"):
                recipient = content_object.author
            elif hasattr(content_object, "patient"):
                recipient = content_object.patient.user

            if recipient != request.user:
                Notification.objects.create(
                    recipient=recipient,
                    notification_type="like",
                    title="إعجاب جديد",
                    message=f"أعجب {request.user.get_full_name()} بـ {content_object}",
                    link=content_object.get_absolute_url(),
                )

        return JsonResponse(
            {
                "status": "success",
                "action": action,
                "likes_count": content_object.likes.count(),
            }
        )
    return JsonResponse({"status": "error"}, status=400)


@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    unread_count = notifications.filter(is_read=False).count()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "unread_count": unread_count,
                "notifications": [
                    {
                        "title": n.title,
                        "message": n.message,
                        "link": n.link,
                        "created_at": n.created_at.strftime("%Y-%m-%d %H:%M"),
                        "is_read": n.is_read,
                    }
                    for n in notifications[:5]
                ],
            }
        )

    return render(
        request,
        "community/notifications.html",
        {"notifications": notifications, "unread_count": unread_count},
    )
