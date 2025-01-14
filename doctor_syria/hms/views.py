from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AdmissionForm,
    AdmissionSearchForm,
    BedForm,
    DateRangeForm,
    DepartmentForm,
    DischargeForm,
    DoctorRoundForm,
    EquipmentForm,
    EquipmentSearchForm,
    InventoryItemForm,
    InventorySearchForm,
    MaintenanceRecordForm,
    NursingRoundForm,
    RoomForm,
    TransferForm,
    WardForm,
)
from .models import (
    Admission,
    Bed,
    Department,
    Discharge,
    DoctorRound,
    Equipment,
    InventoryItem,
    MaintenanceRecord,
    NursingRound,
    Room,
    Transfer,
    Ward,
)


# Dashboard
@login_required
def dashboard(request):
    context = {
        "total_departments": Department.objects.count(),
        "total_patients": Admission.objects.filter(status="admitted").count(),
        "available_beds": Bed.objects.filter(status="available").count(),
        "recent_admissions": Admission.objects.order_by("-admission_date")[:5],
        "low_inventory": InventoryItem.objects.filter(
            quantity__lte=models.F("minimum_quantity")
        ),
        "maintenance_due": Equipment.objects.filter(
            next_maintenance__lte=models.timezone.now().date()
        ),
    }
    return render(request, "hms/dashboard.html", context)


# Department Views
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, "hms/department/list.html", {"departments": departments})


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    context = {
        "department": department,
        "wards": department.ward_set.all(),
        "equipment": department.equipment_set.all(),
        "inventory": department.inventoryitem_set.all(),
    }
    return render(request, "hms/department/detail.html", context)


@login_required
def department_add(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة القسم بنجاح")
            return redirect("hms:department_list")
    else:
        form = DepartmentForm()
    return render(request, "hms/department/form.html", {"form": form})


@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث القسم بنجاح")
            return redirect("hms:department_detail", pk=pk)
    else:
        form = DepartmentForm(instance=department)
    return render(request, "hms/department/form.html", {"form": form})


# Ward Views
@login_required
def ward_list(request):
    wards = Ward.objects.all()
    return render(request, "hms/ward/list.html", {"wards": wards})


@login_required
def ward_detail(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    context = {
        "ward": ward,
        "rooms": ward.room_set.all(),
        "occupancy_rate": (ward.current_occupancy / ward.capacity) * 100,
    }
    return render(request, "hms/ward/detail.html", context)


@login_required
def ward_add(request):
    if request.method == "POST":
        form = WardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة الجناح بنجاح")
            return redirect("hms:ward_list")
    else:
        form = WardForm()
    return render(request, "hms/ward/form.html", {"form": form})


@login_required
def ward_edit(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    if request.method == "POST":
        form = WardForm(request.POST, instance=ward)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الجناح بنجاح")
            return redirect("hms:ward_detail", pk=pk)
    else:
        form = WardForm(instance=ward)
    return render(request, "hms/ward/form.html", {"form": form})


# Room Views
@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, "hms/room/list.html", {"rooms": rooms})


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    context = {
        "room": room,
        "beds": room.bed_set.all(),
        "occupancy_rate": (room.current_occupancy / room.capacity) * 100,
    }
    return render(request, "hms/room/detail.html", context)


@login_required
def room_add(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة الغرفة بنجاح")
            return redirect("hms:room_list")
    else:
        form = RoomForm()
    return render(request, "hms/room/form.html", {"form": form})


@login_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الغرفة بنجاح")
            return redirect("hms:room_detail", pk=pk)
    else:
        form = RoomForm(instance=room)
    return render(request, "hms/room/form.html", {"form": form})


# Admission Views
@login_required
def admission_list(request):
    form = AdmissionSearchForm(request.GET)
    admissions = Admission.objects.all()

    if form.is_valid():
        if form.cleaned_data["patient_name"]:
            admissions = admissions.filter(
                Q(
                    patient__user__first_name__icontains=form.cleaned_data[
                        "patient_name"
                    ]
                )
                | Q(
                    patient__user__last_name__icontains=form.cleaned_data[
                        "patient_name"
                    ]
                )
            )
        if form.cleaned_data["admission_date_from"]:
            admissions = admissions.filter(
                admission_date__gte=form.cleaned_data["admission_date_from"]
            )
        if form.cleaned_data["admission_date_to"]:
            admissions = admissions.filter(
                admission_date__lte=form.cleaned_data["admission_date_to"]
            )
        if form.cleaned_data["status"]:
            admissions = admissions.filter(status=form.cleaned_data["status"])

    paginator = Paginator(admissions, 20)
    page = request.GET.get("page")
    admissions = paginator.get_page(page)

    return render(
        request, "hms/admission/list.html", {"admissions": admissions, "form": form}
    )


@login_required
def admission_detail(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    context = {
        "admission": admission,
        "nursing_rounds": admission.nursinground_set.all().order_by("-round_time"),
        "doctor_rounds": admission.doctorround_set.all().order_by("-round_time"),
        "transfers": admission.transfer_set.all().order_by("-transfer_date"),
    }
    return render(request, "hms/admission/detail.html", context)


@login_required
def admission_add(request):
    if request.method == "POST":
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save()
            bed = admission.bed
            bed.status = "occupied"
            bed.save()
            messages.success(request, "تم إضافة الإدخال بنجاح")
            return redirect("hms:admission_detail", pk=admission.pk)
    else:
        form = AdmissionForm()
    return render(request, "hms/admission/form.html", {"form": form})


@login_required
def admission_edit(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == "POST":
        form = AdmissionForm(request.POST, instance=admission)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الإدخال بنجاح")
            return redirect("hms:admission_detail", pk=pk)
    else:
        form = AdmissionForm(instance=admission)
    return render(request, "hms/admission/form.html", {"form": form})


# Equipment Views
@login_required
def equipment_list(request):
    form = EquipmentSearchForm(request.GET)
    equipment = Equipment.objects.all()

    if form.is_valid():
        if form.cleaned_data["name"]:
            equipment = equipment.filter(name__icontains=form.cleaned_data["name"])
        if form.cleaned_data["department"]:
            equipment = equipment.filter(department=form.cleaned_data["department"])
        if form.cleaned_data["status"]:
            equipment = equipment.filter(status=form.cleaned_data["status"])
        if form.cleaned_data["maintenance_due"]:
            equipment = equipment.filter(
                next_maintenance__lte=models.timezone.now().date()
            )

    return render(
        request, "hms/equipment/list.html", {"equipment": equipment, "form": form}
    )


@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    maintenance_records = equipment.maintenancerecord_set.all().order_by(
        "-maintenance_date"
    )
    return render(
        request,
        "hms/equipment/detail.html",
        {"equipment": equipment, "maintenance_records": maintenance_records},
    )


@login_required
def equipment_add(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, "تم إضافة المعدات بنجاح")
            return redirect("hms:equipment_detail", pk=equipment.pk)
    else:
        form = EquipmentForm()
    return render(request, "hms/equipment/form.html", {"form": form})


@login_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث المعدات بنجاح")
            return redirect("hms:equipment_detail", pk=pk)
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, "hms/equipment/form.html", {"form": form})


# Inventory Views
@login_required
def inventory_list(request):
    form = InventorySearchForm(request.GET)
    inventory = InventoryItem.objects.all()

    if form.is_valid():
        if form.cleaned_data["name"]:
            inventory = inventory.filter(name__icontains=form.cleaned_data["name"])
        if form.cleaned_data["department"]:
            inventory = inventory.filter(department=form.cleaned_data["department"])
        if form.cleaned_data["low_stock"]:
            inventory = inventory.filter(quantity__lte=models.F("minimum_quantity"))

    return render(
        request, "hms/inventory/list.html", {"inventory": inventory, "form": form}
    )


# Report Views
@login_required
def occupancy_report(request):
    form = DateRangeForm(request.GET)
    data = None

    if form.is_valid():
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]

        data = {
            "departments": [],
            "total_beds": 0,
            "occupied_beds": 0,
            "occupancy_rate": 0,
        }

        for dept in Department.objects.all():
            dept_data = {
                "name": dept.name,
                "total_beds": Bed.objects.filter(room__ward__department=dept).count(),
                "occupied_beds": Bed.objects.filter(
                    room__ward__department=dept, status="occupied"
                ).count(),
            }
            dept_data["occupancy_rate"] = (
                (dept_data["occupied_beds"] / dept_data["total_beds"]) * 100
                if dept_data["total_beds"] > 0
                else 0
            )
            data["departments"].append(dept_data)
            data["total_beds"] += dept_data["total_beds"]
            data["occupied_beds"] += dept_data["occupied_beds"]

        data["occupancy_rate"] = (
            (data["occupied_beds"] / data["total_beds"]) * 100
            if data["total_beds"] > 0
            else 0
        )

    return render(request, "hms/reports/occupancy.html", {"form": form, "data": data})


# API Endpoints
@login_required
def bed_availability_api(request):
    data = {"departments": []}

    for dept in Department.objects.all():
        dept_data = {
            "name": dept.name,
            "available_beds": Bed.objects.filter(
                room__ward__department=dept, status="available"
            ).count(),
            "total_beds": Bed.objects.filter(room__ward__department=dept).count(),
        }
        data["departments"].append(dept_data)

    return JsonResponse(data)


@login_required
def department_stats_api(request):
    data = {"departments": []}

    for dept in Department.objects.all():
        dept_data = {
            "name": dept.name,
            "current_patients": Admission.objects.filter(
                bed__room__ward__department=dept, status="admitted"
            ).count(),
            "admissions_today": Admission.objects.filter(
                bed__room__ward__department=dept,
                admission_date__date=models.timezone.now().date(),
            ).count(),
            "discharges_today": Discharge.objects.filter(
                admission__bed__room__ward__department=dept,
                discharge_date__date=models.timezone.now().date(),
            ).count(),
        }
        data["departments"].append(dept_data)

    return JsonResponse(data)


@login_required
def inventory_alerts_api(request):
    low_stock_items = InventoryItem.objects.filter(
        quantity__lte=models.F("minimum_quantity")
    ).values("name", "quantity", "minimum_quantity", "department__name")

    return JsonResponse({"low_stock_items": list(low_stock_items)})
