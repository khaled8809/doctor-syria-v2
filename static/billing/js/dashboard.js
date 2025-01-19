document.addEventListener('DOMContentLoaded', function() {
    // تهيئة الرسوم البيانية
    initCharts();
    
    // تهيئة أدوات التصفية
    initFilters();
    
    // تهيئة التصدير
    initExport();
    
    // تهيئة استرداد المدفوعات
    initRefund();
});

// تهيئة الرسوم البيانية
function initCharts() {
    // رسم بياني للمدفوعات
    const paymentsCtx = document.getElementById('paymentsChart').getContext('2d');
    new Chart(paymentsCtx, {
        type: 'line',
        data: paymentsData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // رسم بياني لطرق الدفع
    const methodsCtx = document.getElementById('paymentMethodsChart').getContext('2d');
    new Chart(methodsCtx, {
        type: 'doughnut',
        data: paymentMethodsData,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// تهيئة أدوات التصفية
function initFilters() {
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const methodFilter = document.getElementById('paymentMethodFilter');
    const dateFilter = document.getElementById('dateFilter');
    
    // البحث
    searchInput.addEventListener('input', filterTable);
    
    // تصفية الحالة
    statusFilter.addEventListener('change', filterTable);
    
    // تصفية طريقة الدفع
    methodFilter.addEventListener('change', filterTable);
    
    // تصفية التاريخ
    dateFilter.addEventListener('change', filterTable);
}

// تصفية الجدول
function filterTable() {
    const searchValue = document.getElementById('searchInput').value.toLowerCase();
    const statusValue = document.getElementById('statusFilter').value;
    const methodValue = document.getElementById('paymentMethodFilter').value;
    const dateValue = document.getElementById('dateFilter').value;
    
    const rows = document.querySelectorAll('#transactionsTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const status = row.querySelector('td:nth-child(5)').textContent.trim();
        const method = row.querySelector('td:nth-child(4)').textContent.trim();
        const date = row.querySelector('td:nth-child(6)').textContent.split(' ')[0];
        
        const matchesSearch = text.includes(searchValue);
        const matchesStatus = !statusValue || status.includes(statusValue);
        const matchesMethod = !methodValue || method.includes(methodValue);
        const matchesDate = !dateValue || date === dateValue;
        
        row.style.display = matchesSearch && matchesStatus && matchesMethod && matchesDate ? '' : 'none';
    });
}

// تهيئة التصدير
function initExport() {
    // تصدير إلى Excel
    document.getElementById('exportExcel').addEventListener('click', exportToExcel);
    
    // تصدير إلى PDF
    document.getElementById('exportPDF').addEventListener('click', exportToPDF);
}

// تصدير إلى Excel
function exportToExcel() {
    const table = document.getElementById('transactionsTable');
    const wb = XLSX.utils.table_to_book(table, { sheet: "المدفوعات" });
    XLSX.writeFile(wb, 'payments.xlsx');
}

// تصدير إلى PDF
function exportToPDF() {
    const doc = new jsPDF();
    doc.autoTable({ html: '#transactionsTable' });
    doc.save('payments.pdf');
}

// تهيئة استرداد المدفوعات
function initRefund() {
    const refundModal = new bootstrap.Modal(document.getElementById('refundModal'));
    
    // فتح نافذة الاسترداد
    document.querySelectorAll('.refund-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const paymentId = this.dataset.paymentId;
            document.getElementById('refundPaymentId').value = paymentId;
            refundModal.show();
        });
    });
    
    // معالجة نموذج الاسترداد
    document.getElementById('confirmRefundBtn').addEventListener('click', async function() {
        const form = document.getElementById('refundForm');
        const formData = new FormData(form);
        
        try {
            const response = await fetch(`/api/billing/payments/${formData.get('payment_id')}/refund/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    amount: formData.get('amount'),
                    reason: formData.get('reason')
                })
            });
            
            if (response.ok) {
                showAlert('تم استرداد المبلغ بنجاح', 'success');
                refundModal.hide();
                location.reload();
            } else {
                throw new Error('فشل استرداد المبلغ');
            }
        } catch (error) {
            showAlert(error.message, 'error');
        }
    });
}

// عرض تنبيه
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container-fluid').insertAdjacentElement('afterbegin', alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// الحصول على CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
