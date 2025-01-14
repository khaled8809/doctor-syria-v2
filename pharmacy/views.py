from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    InventoryForm,
    InventorySearchForm,
    InventoryTransactionForm,
    MedicineForm,
    PrescriptionForm,
    PrescriptionItemForm,
    PrescriptionSearchForm,
)
from .models import (
    Inventory,
    InventoryTransaction,
    Medicine,
    Prescription,
    PrescriptionItem,
)


class PharmacistRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or hasattr(
            self.request.user, "pharmacist_profile"
        )


# Medicine Views
class MedicineListView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = "pharmacy/medicine_list.html"
    context_object_name = "medicines"
    paginate_by = 10

    def get_queryset(self):
        queryset = Medicine.objects.all()
        search = self.request.GET.get("search")
        category = self.request.GET.get("category")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(scientific_name__icontains=search)
            )
        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by("name")


class MedicineCreateView(PharmacistRequiredMixin, CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "pharmacy/medicine_form.html"
    success_url = reverse_lazy("pharmacy:medicine-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "تم إضافة الدواء بنجاح.")
        return response


class MedicineDetailView(LoginRequiredMixin, DetailView):
    model = Medicine
    template_name = "pharmacy/medicine_detail.html"
    context_object_name = "medicine"


class MedicineUpdateView(PharmacistRequiredMixin, UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "pharmacy/medicine_form.html"
    success_url = reverse_lazy("pharmacy:medicine-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "تم تحديث الدواء بنجاح.")
        return response


class MedicineDeleteView(PharmacistRequiredMixin, DeleteView):
    model = Medicine
    template_name = "pharmacy/medicine_confirm_delete.html"
    success_url = reverse_lazy("pharmacy:medicine-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف الدواء بنجاح.")
        return super().delete(request, *args, **kwargs)


# Inventory Views
class InventoryListView(LoginRequiredMixin, ListView):
    model = Inventory
    template_name = "pharmacy/inventory_list.html"
    context_object_name = "inventory_items"
    paginate_by = 10

    def get_queryset(self):
        queryset = Inventory.objects.all()
        form = InventorySearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["search"]:
                search = form.cleaned_data["search"]
                queryset = queryset.filter(
                    Q(medicine__name__icontains=search)
                    | Q(medicine__scientific_name__icontains=search)
                )
            if form.cleaned_data["category"]:
                queryset = queryset.filter(
                    medicine__category=form.cleaned_data["category"]
                )
            if form.cleaned_data["low_stock"]:
                queryset = queryset.filter(quantity__lte=F("minimum_stock"))
            if form.cleaned_data["expired"]:
                queryset = queryset.filter(expiry_date__lt=timezone.now().date())

        return queryset.order_by("medicine__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = InventorySearchForm(self.request.GET)
        return context


class InventoryAddView(PharmacistRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = "pharmacy/inventory_form.html"
    success_url = reverse_lazy("pharmacy:inventory-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        # إنشاء سجل حركة مخزون
        InventoryTransaction.objects.create(
            inventory=form.instance,
            transaction_type="in",
            quantity=form.instance.quantity,
            reference="Initial Stock",
            performed_by=self.request.user,
        )

        messages.success(self.request, "تم إضافة المخزون بنجاح.")
        return response


# Prescription Views
class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = "pharmacy/prescription_list.html"
    context_object_name = "prescriptions"
    paginate_by = 10

    def get_queryset(self):
        queryset = Prescription.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(patient=self.request.user) | Q(doctor=self.request.user)
            )

        form = PrescriptionSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data["search"]:
                search = form.cleaned_data["search"]
                queryset = queryset.filter(
                    Q(patient__first_name__icontains=search)
                    | Q(patient__last_name__icontains=search)
                    | Q(doctor__first_name__icontains=search)
                    | Q(doctor__last_name__icontains=search)
                )
            if form.cleaned_data["status"]:
                queryset = queryset.filter(status=form.cleaned_data["status"])
            if form.cleaned_data["date_from"]:
                queryset = queryset.filter(
                    date_prescribed__gte=form.cleaned_data["date_from"]
                )
            if form.cleaned_data["date_to"]:
                queryset = queryset.filter(
                    date_prescribed__lte=form.cleaned_data["date_to"]
                )

        return queryset.order_by("-date_prescribed")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PrescriptionSearchForm(self.request.GET)
        return context


class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "pharmacy/prescription_form.html"
    success_url = reverse_lazy("pharmacy:prescription-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["items_formset"] = PrescriptionItemFormSet(self.request.POST)
        else:
            context["items_formset"] = PrescriptionItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context["items_formset"]

        if items_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.doctor = self.request.user
            self.object.save()

            items_formset.instance = self.object
            items_formset.save()

            messages.success(self.request, "تم إنشاء الوصفة الطبية بنجاح.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PrescriptionDetailView(LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = "pharmacy/prescription_detail.html"
    context_object_name = "prescription"

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(patient=self.request.user) | Q(doctor=self.request.user)
            )
        return queryset


class PrescriptionDispenseView(PharmacistRequiredMixin, UpdateView):
    model = Prescription
    template_name = "pharmacy/prescription_dispense.html"
    fields = []
    success_url = reverse_lazy("pharmacy:prescription-list")

    def post(self, request, *args, **kwargs):
        prescription = self.get_object()

        if prescription.status != "pending":
            messages.error(request, "لا يمكن صرف هذه الوصفة الطبية.")
            return redirect("pharmacy:prescription-detail", pk=prescription.pk)

        # التحقق من توفر جميع الأدوية
        for item in prescription.items.all():
            if item.medicine.inventory.quantity < item.quantity:
                messages.error(
                    request,
                    f"الكمية المطلوبة من {item.medicine.name} غير متوفرة في المخزون.",
                )
                return redirect("pharmacy:prescription-detail", pk=prescription.pk)

        # صرف الأدوية وتحديث المخزون
        for item in prescription.items.all():
            inventory = item.medicine.inventory
            inventory.quantity -= item.quantity
            inventory.save()

            # تسجيل حركة المخزون
            InventoryTransaction.objects.create(
                inventory=inventory,
                transaction_type="out",
                quantity=item.quantity,
                reference=f"Prescription #{prescription.pk}",
                performed_by=request.user,
            )

        # تحديث حالة الوصفة
        prescription.status = "dispensed"
        prescription.dispensed_by = request.user
        prescription.dispensed_date = timezone.now()
        prescription.save()

        messages.success(request, "تم صرف الوصفة الطبية بنجاح.")
        return redirect("pharmacy:prescription-list")


class PrescriptionUpdateView(LoginRequiredMixin, PharmacistRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "pharmacy/prescription_form.html"
    success_url = reverse_lazy("pharmacy:prescription-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["items_formset"] = PrescriptionItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["items_formset"] = PrescriptionItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context["items_formset"]
        if form.is_valid() and items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            messages.success(self.request, "تم تحديث الوصفة الطبية بنجاح.")
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class PrescriptionDeleteView(LoginRequiredMixin, PharmacistRequiredMixin, DeleteView):
    model = Prescription
    template_name = "pharmacy/prescription_confirm_delete.html"
    success_url = reverse_lazy("pharmacy:prescription-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف الوصفة الطبية بنجاح.")
        return super().delete(request, *args, **kwargs)


# Report Views
class InventoryReportView(PharmacistRequiredMixin, TemplateView):
    template_name = "pharmacy/inventory_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # إحصائيات المخزون
        context["total_items"] = Inventory.objects.count()
        context["low_stock_items"] = Inventory.objects.filter(
            quantity__lte=F("minimum_stock")
        ).count()
        context["expired_items"] = Inventory.objects.filter(
            expiry_date__lt=timezone.now().date()
        ).count()

        # قيمة المخزون
        context["total_value"] = (
            Inventory.objects.aggregate(
                total=Sum(F("quantity") * F("medicine__price"))
            )["total"]
            or 0
        )

        # حركات المخزون الأخيرة
        context["recent_transactions"] = InventoryTransaction.objects.all()[:10]

        return context


class LowStockView(PharmacistRequiredMixin, ListView):
    template_name = "pharmacy/low_stock.html"
    context_object_name = "items"

    def get_queryset(self):
        return Inventory.objects.filter(quantity__lte=F("minimum_stock")).order_by(
            "medicine__name"
        )
