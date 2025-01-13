/**
 * نظام عرض التقارير والرسوم البيانية
 */

// تهيئة Chart.js مع الإعدادات العربية
Chart.defaults.font.family = 'Cairo, sans-serif';
Chart.defaults.font.size = 14;

class ReportViewer {
    constructor() {
        this.charts = {};
        this.currentReport = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // استمع لتغييرات التصفية
        document.querySelectorAll('.report-filter').forEach(filter => {
            filter.addEventListener('change', () => this.refreshReport());
        });

        // استمع لأزرار التصدير
        document.querySelectorAll('.export-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const format = e.target.dataset.format;
                this.exportReport(format);
            });
        });
    }

    async loadReport(reportType, params = {}) {
        try {
            const response = await fetch(`/api/reports/${reportType}/?${new URLSearchParams(params)}`);
            const data = await response.json();
            this.currentReport = { type: reportType, data };
            this.displayReport(data);
        } catch (error) {
            console.error('خطأ في تحميل التقرير:', error);
            this.showError('حدث خطأ أثناء تحميل التقرير');
        }
    }

    displayReport(data) {
        // تنظيف العروض السابقة
        this.clearCharts();

        // عرض البيانات حسب نوع التقرير
        switch (this.currentReport.type) {
            case 'patient_progress':
                this.displayPatientProgress(data);
                break;
            case 'clinic_statistics':
                this.displayClinicStatistics(data);
                break;
            case 'health_metrics':
                this.displayHealthMetrics(data);
                break;
            default:
                this.displayGenericReport(data);
        }
    }

    displayPatientProgress(data) {
        // عرض معلومات المريض
        document.getElementById('patient-info').innerHTML = `
            <h3>معلومات المريض</h3>
            <p>الاسم: ${data.patient_info.name}</p>
            <p>الفترة: ${data.period.start} - ${data.period.end}</p>
        `;

        // رسم بياني للمقاييس الصحية
        const metricsCanvas = document.getElementById('metrics-chart');
        this.charts.metrics = new Chart(metricsCanvas, {
            type: 'line',
            data: this.prepareMetricsData(data.metrics),
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'تطور المقاييس الصحية'
                    }
                }
            }
        });

        // رسم بياني لتقدم العلاج
        const progressCanvas = document.getElementById('progress-chart');
        this.charts.progress = new Chart(progressCanvas, {
            type: 'pie',
            data: this.prepareProgressData(data.progress.trend),
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'توزيع حالات التقدم'
                    }
                }
            }
        });
    }

    displayClinicStatistics(data) {
        // رسم بياني للمواعيد
        const appointmentsCanvas = document.getElementById('appointments-chart');
        this.charts.appointments = new Chart(appointmentsCanvas, {
            type: 'bar',
            data: this.prepareAppointmentsData(data.appointments),
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'إحصائيات المواعيد'
                    }
                }
            }
        });

        // عرض إحصائيات المرضى
        document.getElementById('patients-stats').innerHTML = `
            <h3>إحصائيات المرضى</h3>
            <p>العدد الكلي: ${data.patients.unique}</p>
            <p>المرضى الجدد: ${data.patients.new}</p>
        `;
    }

    displayHealthMetrics(data) {
        const trendsCanvas = document.getElementById('trends-chart');
        this.charts.trends = new Chart(trendsCanvas, {
            type: 'line',
            data: this.prepareTrendsData(data.trends),
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'اتجاهات المؤشرات الصحية'
                    }
                }
            }
        });
    }

    prepareMetricsData(metrics) {
        const datasets = [];
        for (const [type, data] of Object.entries(metrics)) {
            datasets.push({
                label: this.getMetricLabel(type),
                data: data.values,
                borderColor: this.getMetricColor(type),
                fill: false
            });
        }
        return { datasets };
    }

    prepareProgressData(trend) {
        return {
            labels: trend.map(t => this.getStatusLabel(t.status)),
            datasets: [{
                data: trend.map(t => t.count),
                backgroundColor: trend.map(t => this.getStatusColor(t.status))
            }]
        };
    }

    prepareAppointmentsData(appointments) {
        return {
            labels: Object.keys(appointments.status_distribution).map(this.getStatusLabel),
            datasets: [{
                label: 'عدد المواعيد',
                data: Object.values(appointments.status_distribution),
                backgroundColor: Object.keys(appointments.status_distribution).map(this.getStatusColor)
            }]
        };
    }

    prepareTrendsData(trends) {
        return {
            labels: Object.keys(trends.daily_avg),
            datasets: [{
                label: 'المتوسط اليومي',
                data: Object.values(trends.daily_avg),
                borderColor: '#4CAF50',
                fill: false
            }]
        };
    }

    getMetricLabel(type) {
        const labels = {
            blood_pressure: 'ضغط الدم',
            heart_rate: 'معدل ضربات القلب',
            temperature: 'درجة الحرارة',
            weight: 'الوزن',
            blood_sugar: 'سكر الدم',
            oxygen_level: 'مستوى الأكسجين'
        };
        return labels[type] || type;
    }

    getStatusLabel(status) {
        const labels = {
            scheduled: 'مجدول',
            completed: 'مكتمل',
            cancelled: 'ملغي',
            improving: 'تحسن',
            stable: 'مستقر',
            deteriorating: 'تدهور'
        };
        return labels[status] || status;
    }

    getMetricColor(type) {
        const colors = {
            blood_pressure: '#FF5722',
            heart_rate: '#E91E63',
            temperature: '#9C27B0',
            weight: '#673AB7',
            blood_sugar: '#3F51B5',
            oxygen_level: '#2196F3'
        };
        return colors[type] || '#000000';
    }

    getStatusColor(status) {
        const colors = {
            scheduled: '#2196F3',
            completed: '#4CAF50',
            cancelled: '#F44336',
            improving: '#4CAF50',
            stable: '#FFC107',
            deteriorating: '#FF5722'
        };
        return colors[status] || '#9E9E9E';
    }

    async exportReport(format) {
        if (!this.currentReport) {
            this.showError('لا يوجد تقرير لتصديره');
            return;
        }

        try {
            const response = await fetch('/api/reports/export/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    report_type: this.currentReport.type,
                    format: format,
                    data: this.currentReport.data
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `report_${this.currentReport.type}_${new Date().toISOString()}.${format}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            } else {
                throw new Error('فشل تصدير التقرير');
            }
        } catch (error) {
            console.error('خطأ في تصدير التقرير:', error);
            this.showError('حدث خطأ أثناء تصدير التقرير');
        }
    }

    clearCharts() {
        Object.values(this.charts).forEach(chart => chart.destroy());
        this.charts = {};
    }

    showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

    refreshReport() {
        if (this.currentReport) {
            const filters = {};
            document.querySelectorAll('.report-filter').forEach(filter => {
                filters[filter.name] = filter.value;
            });
            this.loadReport(this.currentReport.type, filters);
        }
    }
}
