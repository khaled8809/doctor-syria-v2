// المتغيرات العامة
let invoiceData = null;

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    const invoiceId = getInvoiceIdFromUrl();
    loadInvoiceDetails(invoiceId);
    
    // إضافة مستمعي الأحداث
    document.getElementById('printInvoiceBtn').addEventListener('click', printInvoice);
    document.getElementById('downloadPdfBtn').addEventListener('click', () => downloadPdf(invoiceId));
    document.getElementById('editInvoiceBtn').addEventListener('click', () => editInvoice(invoiceId));
    document.getElementById('processPaymentBtn')?.addEventListener('click', showPaymentModal);
    document.getElementById('confirmPaymentBtn').addEventListener('click', processPayment);
});

// تحميل تفاصيل الفاتورة
async function loadInvoiceDetails(invoiceId) {
    try {
        const response = await fetch(`/api/billing/invoices/${invoiceId}/`);
        invoiceData = await response.json();
        
        renderInvoiceDetails();
        renderItems();
        renderPayments();
        
        if (invoiceData.payment_method === 'insurance') {
            loadInsuranceInfo(invoiceId);
        }
    } catch (error) {
        showAlert('حدث خطأ أثناء تحميل تفاصيل الفاتورة', 'error');
    }
}

// عرض تفاصيل الفاتورة
function renderInvoiceDetails() {
    document.getElementById('invoiceNumber').textContent = invoiceData.invoice_number;
    document.getElementById('patientName').textContent = invoiceData.patient_name;
    document.getElementById('doctorName').textContent = invoiceData.doctor_name;
    document.getElementById('createdAt').textContent = formatDate(invoiceData.created_at);
    document.getElementById('dueDate').textContent = formatDate(invoiceData.due_date);
    
    const statusBadge = document.getElementById('invoiceStatus');
    statusBadge.textContent = invoiceData.status_display;
    statusBadge.className = `badge bg-${getStatusColor(invoiceData.status)}`;
    
    document.getElementById('paymentMethod').textContent = invoiceData.payment_method_display;
    
    // تحديث المبالغ
    document.getElementById('subtotal').textContent = formatCurrency(invoiceData.subtotal);
    document.getElementById('tax').textContent = formatCurrency(invoiceData.tax);
    document.getElementById('discount').textContent = formatCurrency(invoiceData.discount);
    document.getElementById('total').textContent = formatCurrency(invoiceData.total);
    
    // إخفاء/إظهار زر معالجة الدفع
    const processPaymentBtn = document.getElementById('processPaymentBtn');
    if (processPaymentBtn) {
        processPaymentBtn.style.display = invoiceData.status === 'paid' ? 'none' : 'block';
    }
}

// عرض عناصر الفاتورة
function renderItems() {
    const tbody = document.getElementById('invoiceItems');
    tbody.innerHTML = '';
    
    invoiceData.items.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.description}</td>
            <td>${item.quantity}</td>
            <td>${formatCurrency(item.unit_price)}</td>
            <td>${formatCurrency(item.total_price)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// عرض سجل المدفوعات
async function renderPayments() {
    try {
        const response = await fetch(`/api/billing/payments/?invoice=${invoiceData.id}`);
        const payments = await response.json();
        
        const container = document.getElementById('paymentsHistory');
        container.innerHTML = '';
        
        if (payments.length === 0) {
            container.innerHTML = '<p class="text-muted">لا توجد مدفوعات</p>';
            return;
        }
        
        payments.forEach(payment => {
            const div = document.createElement('div');
            div.className = 'mb-3 p-3 border rounded';
            div.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span>${formatCurrency(payment.amount)}</span>
                    <span class="badge bg-${getStatusColor(payment.status)}">${payment.status_display}</span>
                </div>
                <div class="text-muted small">
                    ${payment.payment_method_display} - ${formatDate(payment.created_at)}
                </div>
                ${payment.notes ? `<div class="mt-2 small">${payment.notes}</div>` : ''}
            `;
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading payments:', error);
    }
}

// تحميل معلومات التأمين
async function loadInsuranceInfo(invoiceId) {
    try {
        const response = await fetch(`/api/billing/insurance-claims/?invoice=${invoiceId}`);
        const claims = await response.json();
        
        if (claims.length > 0) {
            const claim = claims[0];
            document.getElementById('insuranceSection').style.display = 'block';
            document.getElementById('insuranceInfo').innerHTML = `
                <div class="mb-2">
                    <strong>شركة التأمين:</strong>
                    <span>${claim.insurance_provider_name}</span>
                </div>
                <div class="mb-2">
                    <strong>رقم المطالبة:</strong>
                    <span>${claim.claim_number}</span>
                </div>
                <div class="mb-2">
                    <strong>الحالة:</strong>
                    <span class="badge bg-${getStatusColor(claim.status)}">${claim.status_display}</span>
                </div>
                <div class="mb-2">
                    <strong>المبلغ المطالب به:</strong>
                    <span>${formatCurrency(claim.amount_claimed)}</span>
                </div>
                ${claim.amount_approved ? `
                    <div class="mb-2">
                        <strong>المبلغ المعتمد:</strong>
                        <span>${formatCurrency(claim.amount_approved)}</span>
                    </div>
                ` : ''}
            `;
        }
    } catch (error) {
        console.error('Error loading insurance info:', error);
    }
}

// طباعة الفاتورة
function printInvoice() {
    window.print();
}

// تحميل PDF
async function downloadPdf(invoiceId) {
    try {
        const response = await fetch(`/api/billing/invoices/${invoiceId}/generate_pdf/`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `invoice_${invoiceData.invoice_number}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        showAlert('حدث خطأ أثناء تحميل PDF', 'error');
    }
}

// إظهار نموذج الدفع
function showPaymentModal() {
    const amountInput = document.querySelector('#processPaymentForm input[name="amount"]');
    amountInput.value = invoiceData.total;
    $('#processPaymentModal').modal('show');
}

// معالجة الدفع
async function processPayment() {
    try {
        const form = document.getElementById('processPaymentForm');
        const formData = new FormData(form);
        
        const response = await fetch(`/api/billing/invoices/${invoiceData.id}/process_payment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                payment_method: formData.get('payment_method'),
                amount: formData.get('amount'),
                notes: formData.get('notes')
            })
        });
        
        if (response.ok) {
            showAlert('تم معالجة الدفع بنجاح', 'success');
            $('#processPaymentModal').modal('hide');
            loadInvoiceDetails(invoiceData.id);
        } else {
            throw new Error('فشل معالجة الدفع');
        }
    } catch (error) {
        showAlert('حدث خطأ أثناء معالجة الدفع', 'error');
    }
}

// دوال مساعدة
function getInvoiceIdFromUrl() {
    return window.location.pathname.split('/').filter(Boolean).pop();
}

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
