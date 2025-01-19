// تهيئة WebSocket للتحديثات المباشرة
const socket = new WebSocket(
    `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/monitoring/`
);

// المخططات
let charts = {
    cpuUsage: null,
    memoryUsage: null,
    diskUsage: null,
    dbConnections: null,
    activeUsers: null,
    dailyAppointments: null,
    pendingRecords: null
};

// تهيئة المخططات
function initializeCharts() {
    // مخطط CPU
    charts.cpuUsage = new Chart(
        document.querySelector('#cpu-usage .gauge-chart'),
        createGaugeConfig('استخدام CPU')
    );

    // مخطط الذاكرة
    charts.memoryUsage = new Chart(
        document.querySelector('#memory-usage .gauge-chart'),
        createGaugeConfig('استخدام الذاكرة')
    );

    // مخطط القرص
    charts.diskUsage = new Chart(
        document.querySelector('#disk-usage .gauge-chart'),
        createGaugeConfig('استخدام القرص')
    );

    // مخطط اتصالات قاعدة البيانات
    charts.dbConnections = new Chart(
        document.querySelector('#db-connections .line-chart'),
        createLineConfig('اتصالات قاعدة البيانات')
    );

    // مخطط المستخدمين النشطين
    charts.activeUsers = new Chart(
        document.querySelector('#active-users-chart'),
        createLineConfig('المستخدمون النشطون')
    );

    // مخطط المواعيد اليومية
    charts.dailyAppointments = new Chart(
        document.querySelector('#daily-appointments-chart'),
        createBarConfig('المواعيد اليومية')
    );

    // مخطط السجلات المعلقة
    charts.pendingRecords = new Chart(
        document.querySelector('#pending-records-chart'),
        createBarConfig('السجلات المعلقة')
    );
}

// إنشاء تكوين مخطط المقياس
function createGaugeConfig(label) {
    return {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: ['#4CAF50', '#ecf0f1']
            }]
        },
        options: {
            circumference: 180,
            rotation: -90,
            cutout: '80%',
            plugins: {
                title: {
                    display: true,
                    text: label
                }
            }
        }
    };
}

// إنشاء تكوين المخطط الخطي
function createLineConfig(label) {
    return {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: [],
                borderColor: '#3498db',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    };
}

// إنشاء تكوين المخطط الشريطي
function createBarConfig(label) {
    return {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: [],
                backgroundColor: '#3498db'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    };
}

// تحديث المخططات
function updateCharts(data) {
    // تحديث مقاييس النظام
    updateGaugeChart(charts.cpuUsage, data.metrics.cpu_usage);
    updateGaugeChart(charts.memoryUsage, data.metrics.memory_usage);
    updateGaugeChart(charts.diskUsage, data.metrics.disk_usage);
    
    // تحديث مخطط اتصالات قاعدة البيانات
    updateLineChart(charts.dbConnections, data.metrics.db_connections);
    
    // تحديث مخططات الأداء
    updateLineChart(charts.activeUsers, data.metrics.active_users);
    updateBarChart(charts.dailyAppointments, data.metrics.total_appointments_today);
    updateBarChart(charts.pendingRecords, data.metrics.pending_medical_records);
}

// تحديث مخطط المقياس
function updateGaugeChart(chart, value) {
    chart.data.datasets[0].data = [value, 100 - value];
    chart.update();
}

// تحديث المخطط الخطي
function updateLineChart(chart, value) {
    const now = moment().format('HH:mm:ss');
    
    chart.data.labels.push(now);
    chart.data.datasets[0].data.push(value);
    
    // الاحتفاظ بآخر 10 قيم فقط
    if (chart.data.labels.length > 10) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    
    chart.update();
}

// تحديث المخطط الشريطي
function updateBarChart(chart, value) {
    const now = moment().format('HH:mm');
    
    chart.data.labels.push(now);
    chart.data.datasets[0].data.push(value);
    
    // الاحتفاظ بآخر 8 قيم فقط
    if (chart.data.labels.length > 8) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    
    chart.update();
}

// تحديث قائمة التنبيهات
function updateAlerts(alerts) {
    const alertsList = document.getElementById('alerts-list');
    alertsList.innerHTML = '';
    
    alerts.forEach(alert => {
        const alertElement = document.createElement('div');
        alertElement.className = `alert-item ${alert.level}`;
        alertElement.innerHTML = `
            <div class="alert-time">${moment(alert.timestamp).format('HH:mm:ss')}</div>
            <div class="alert-message">${alert.message}</div>
        `;
        alertsList.appendChild(alertElement);
    });
}

// معالجة أحداث WebSocket
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'system_metrics') {
        updateCharts(data);
    } else if (data.type === 'system_alerts') {
        updateAlerts(data.alerts);
    }
};

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    
    // تحديث البيانات الأولية
    fetch('/api/monitoring/system-status/')
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
        });
    
    // تحديث التنبيهات الأولية
    fetch('/api/monitoring/recent-alerts/')
        .then(response => response.json())
        .then(data => {
            updateAlerts(data);
        });
});
