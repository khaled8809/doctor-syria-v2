from django import forms

from .models import Answer, Comment, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content", "category", "tags", "is_anonymous"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "اكتب عنوان سؤالك هنا"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "اشرح سؤالك بالتفصيل",
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل الكلمات المفتاحية مفصولة بفواصل",
                }
            ),
            "is_anonymous": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "عنوان السؤال",
            "content": "تفاصيل السؤال",
            "category": "التصنيف",
            "tags": "الكلمات المفتاحية",
            "is_anonymous": "نشر السؤال بشكل مجهول",
        }
        help_texts = {
            "tags": "مثال: سكري, ضغط الدم, تغذية",
            "is_anonymous": "لن يظهر اسمك للزوار إذا اخترت هذا الخيار",
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "اكتب إجابتك هنا",
                }
            )
        }
        labels = {"content": "الإجابة"}


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
