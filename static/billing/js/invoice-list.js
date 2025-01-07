// المتغيرات العامة
let currentPage = 1;
const itemsPerPage = 10;

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    loadInvoices();
    loadStats();
    initializeForm();
    
    // إضافة مستمعي الأحداث
    document.getElementById('searchInvoice').addEventListener('input', debounce(loadInvoices, 500));
    document.getElementById('addItemBtn').addEventListener('click', addInvoiceItem);
    document.getElementById('saveInvoiceBtn').addEventListener('click', saveInvoice);
});

// تحميل الفواتير
async function loadInvoices() {
    try {
        const searchQuery = document.getElementById('searchInvoice').value;
        const response = await fetch(`/api/billing/invoices/?page=${currentPage}&search=${searchQuery}`);
        const data = await response.json();
        
        renderInvoices(data.results);
        renderPagination(data.count);
    } catch (error) {
        showAlert('حدث خطأ أثناء تحميل الفواتير', 'error');
    }
}

// تحميل الإحصائيات
async function loadStats() {
    try {
        const response = await fetch('/api/billing/invoices/stats/');
        const data = await response.json();
        
        document.getElementById('totalInvoices').textContent = data.total;
        document.getElementById('paidInvoices').textContent = data.paid;
        document.getElementById('pendingInvoices').textContent = data.pending;
        document.getElementById('overdueInvoices').textContent = data.overdue;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// عرض الفواتير في الجدول
function renderInvoices(invoices) {
    const tbody = document.getElementById('invoicesTableBody');
    tbody.innerHTML = '';
    
    invoices.forEach(invoice => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${invoice.invoice_number}</td>
            <td>${invoice.patient_name}</td>
            <td>${invoice.doctor_name}</td>
            <td>${formatDate(invoice.created_at)}</td>
            <td>${formatCurrency(invoice.total)}</td>
            <td><span class="badge bg-${getStatusColor(invoice.status)}">${invoice.status_display}</span></td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-primary" onclick="viewInvoice('${invoice.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-success" onclick="downloadPdf('${invoice.id}')">
                        <i class="fas fa-file-pdf"></i>
                    </button>
                    ${invoice.status === 'draft' ? `
                        <button class="btn btn-warning" onclick="editInvoice('${invoice.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                    ` : ''}
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// عرض أزرار الصفحات
function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const pagination = document.getElementById('invoicesPagination');
    pagination.innerHTML = '';
    
    // زر السابق
    pagination.innerHTML += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage - 1})">السابق</a>
        </li>
    `;
    
    // أزرار الصفحات
    for (let i = 1; i <= totalPages; i++) {
        pagination.innerHTML += `
            <li class="page-item ${currentPage === i ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
            </li>
        `;
    }
    
    // زر التالي
    pagination.innerHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage + 1})">التالي</a>
        </li>
    `;
}

// تغيير الصفحة
function changePage(page) {
    currentPage = page;
    loadInvoices();
}

// تهيئة نموذج إنشاء الفاتورة
async function initializeForm() {
    try {
        // تحميل قائمة المرضى
        const patientsResponse = await fetch('/api/medical_records/patients/');
        const patients = await patientsResponse.json();
        const patientSelect = document.querySelector('select[name="patient"]');
        patients.forEach(patient => {
            patientSelect.innerHTML += `<option value="${patient.id}">${patient.user.full_name}</option>`;
        });
        
        // تحميل قائمة الأطباء
        const doctorsResponse = await fetch('/api/accounts/doctors/');
        const doctors = await doctorsResponse.json();
        const doctorSelect = document.querySelector('select[name="doctor"]');
        doctors.forEach(doctor => {
            doctorSelect.innerHTML += `<option value="${doctor.id}">${doctor.user.full_name}</option>`;
        });
    } catch (error) {
        showAlert('حدث خطأ أثناء تحميل البيانات', 'error');
    }
}

// إضافة عنصر للفاتورة
function addInvoiceItem() {
    const itemsContainer = document.getElementById('invoiceItems');
    const itemDiv = document.createElement('div');
    itemDiv.className = 'row mb-2';
    itemDiv.innerHTML = `
        <div class="col-5">
            <input type="text" class="form-control" name="description[]" placeholder="الوصف" required>
        </div>
        <div class="col-2">
            <input type="number" class="form-control" name="quantity[]" value="1" min="1" required>
        </div>
        <div class="col-3">
            <input type="number" class="form-control" name="unit_price[]" step="0.01" required>
        </div>
        <div class="col-2">
            <button type="button" class="btn btn-danger btn-sm" onclick="removeInvoiceItem(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    itemsContainer.appendChild(itemDiv);
}

// حذف عنصر من الفاتورة
function removeInvoiceItem(button) {
    button.closest('.row').remove();
    calculateTotal();
}

// حساب المجموع
function calculateTotal() {
    const quantities = document.getElementsByName('quantity[]');
    const prices = document.getElementsByName('unit_price[]');
    let subtotal = 0;
    
    for (let i = 0; i < quantities.length; i++) {
        subtotal += quantities[i].value * prices[i].value;
    }
    
    const tax = subtotal * 0.15; // 15% ضريبة
    const discount = document.querySelector('input[name="discount"]').value || 0;
    const total = subtotal + tax - discount;
    
    document.querySelector('input[name="subtotal"]').value = subtotal.toFixed(2);
    document.querySelector('input[name="tax"]').value = tax.toFixed(2);
    document.querySelector('input[name="total"]').value = total.toFixed(2);
}

// حفظ الفاتورة
async function saveInvoice() {
    try {
        const form = document.getElementById('createInvoiceForm');
        const formData = new FormData(form);
        
        // تحويل البيانات إلى JSON
        const data = {
            patient: formData.get('patient'),
            doctor: formData.get('doctor'),
            due_date: formData.get('due_date'),
            payment_method: formData.get('payment_method'),
            subtotal: formData.get('subtotal'),
            tax: formData.get('tax'),
            discount: formData.get('discount'),
            notes: formData.get('notes'),
            items: []
        };
        
        // إضافة العناصر
        const descriptions = formData.getAll('description[]');
        const quantities = formData.getAll('quantity[]');
        const prices = formData.getAll('unit_price[]');
        
        for (let i = 0; i < descriptions.length; i++) {
            data.items.push({
                description: descriptions[i],
                quantity: quantities[i],
                unit_price: prices[i]
            });
        }
        
        // إرسال البيانات
        const response = await fetch('/api/billing/invoices/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('تم إنشاء الفاتورة بنجاح', 'success');
            $('#createInvoiceModal').modal('hide');
            loadInvoices();
            loadStats();
        } else {
            throw new Error('فشل إنشاء الفاتورة');
        }
    } catch (error) {
        showAlert('حدث خطأ أثناء حفظ الفاتورة', 'error');
    }
}

// دوال مساعدة
function formatDate(date) {
    return new Date(date).toLocaleDateString('ar-SA');
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'SAR'
    }).format(amount);
}

function getStatusColor(status) {
    const colors = {
        'draft': 'secondary',
        'pending': 'warning',
        'paid': 'success',
        'cancelled': 'danger',
        'refunded': 'info'
    };
    return colors[status] || 'secondary';
}

function showAlert(message, type) {
    // يمكن استخدام مكتبة مثل SweetAlert2 أو Toastr
    alert(message);
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
