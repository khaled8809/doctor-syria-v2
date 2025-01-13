from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView, TemplateView

from accounts.models import Area, Clinic, Doctor, Hospital

from .models import Article, Review


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clinics"] = Clinic.objects.all()[:3]
        context["hospitals"] = Hospital.objects.all()[:2]
        context["articles"] = Article.objects.filter(is_published=True)[:3]
        context["reviews"] = Review.objects.filter(is_approved=True)[:5]
        context["areas"] = Area.objects.all()
        return context


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


@csrf_protect
def search_view(request):
    if request.method == "POST":
        search_type = request.POST.get("type")
        query = request.POST.get("query")
        specialization = request.POST.get("specialization")
        area = request.POST.get("area")

        results = []

        if search_type == "doctor":
            doctors = Doctor.objects.all()
            if query:
                doctors = doctors.filter(
                    Q(user__first_name__icontains=query)
                    | Q(user__last_name__icontains=query)
                )
            if specialization:
                doctors = doctors.filter(specialization=specialization)

            results = [
                {
                    "id": doctor.id,
                    "name": f"{doctor.user.first_name} {doctor.user.last_name}",
                    "type": "doctor",
                    "specialization": doctor.specialization,
                    "clinic_name": doctor.clinic.name if doctor.clinic else None,
                    "rating": doctor.average_rating,
                    "description": doctor.bio,
                }
                for doctor in doctors
            ]

        elif search_type in ["clinic", "hospital"]:
            model = Clinic if search_type == "clinic" else Hospital
            locations = model.objects.all()

            if query:
                locations = locations.filter(name__icontains=query)
            if area:
                locations = locations.filter(area=area)

            results = [
                {
                    "id": location.id,
                    "name": location.name,
                    "type": search_type,
                    "address": location.address,
                    "phone": location.phone,
                    "rating": location.average_rating,
                    "description": location.description,
                }
                for location in locations
            ]

        return JsonResponse(results, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_protect
def contact_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # هنا يمكنك إضافة منطق لحفظ بيانات نموذج الاتصال
        # أو إرسال إشعارات بالبريد الإلكتروني

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def get_medical_locations(request, area_id):
    clinics = Clinic.objects.filter(area_id=area_id)
    hospitals = Hospital.objects.filter(area_id=area_id)

    data = []

    for clinic in clinics:
        data.append(
            {
                "id": clinic.id,
                "name": clinic.name,
                "type": "clinic",
                "address": clinic.address,
                "latitude": (
                    float(clinic.latitude) if hasattr(clinic, "latitude") else None
                ),
                "longitude": (
                    float(clinic.longitude) if hasattr(clinic, "longitude") else None
                ),
            }
        )

    for hospital in hospitals:
        data.append(
            {
                "id": hospital.id,
                "name": hospital.name,
                "type": "hospital",
                "address": hospital.address,
                "latitude": (
                    float(hospital.latitude) if hasattr(hospital, "latitude") else None
                ),
                "longitude": (
                    float(hospital.longitude)
                    if hasattr(hospital, "longitude")
                    else None
                ),
            }
        )

    return JsonResponse(data, safe=False)
