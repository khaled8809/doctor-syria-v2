from django import forms

from .models import Comment, Event, Group, HealthTip, Post, Story


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "image", "is_private"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "اسم المجموعة",
            "description": "وصف المجموعة",
            "image": "صورة المجموعة",
            "is_private": "مجموعة خاصة",
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "عنوان المنشور",
            "content": "محتوى المنشور",
            "image": "صورة (اختياري)",
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "image",
            "location",
            "start_date",
            "end_date",
            "max_participants",
            "is_online",
            "meeting_link",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "max_participants": forms.NumberInput(attrs={"class": "form-control"}),
            "is_online": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "meeting_link": forms.URLInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "عنوان الفعالية",
            "description": "وصف الفعالية",
            "image": "صورة الفعالية",
            "location": "المكان",
            "start_date": "تاريخ ووقت البداية",
            "end_date": "تاريخ ووقت النهاية",
            "max_participants": "الحد الأقصى للمشاركين",
            "is_online": "فعالية عبر الإنترنت",
            "meeting_link": "رابط الاجتماع (للفعاليات عبر الإنترنت)",
        }


class HealthTipForm(forms.ModelForm):
    class Meta:
        model = HealthTip
        fields = ["title", "content", "image", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "عنوان النصيحة",
            "content": "محتوى النصيحة",
            "image": "صورة (اختياري)",
            "category": "التصنيف",
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "content", "condition", "image", "is_anonymous"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "condition": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_anonymous": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "عنوان القصة",
            "content": "محتوى القصة",
            "condition": "الحالة الصحية",
            "image": "صورة (اختياري)",
            "is_anonymous": "نشر بشكل مجهول",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "اكتب تعليقك هنا",
                }
            )
        }
        labels = {"content": "التعليق"}
