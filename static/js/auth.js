// التحقق مما إذا كان المستخدم مسجل الدخول
function checkAuth() {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        const user = JSON.parse(currentUser);
        updateNavbar(user);
        return true;
    }
    return false;
}

// تحديث شريط التنقل بناءً على حالة تسجيل الدخول
function updateNavbar(user) {
    const authNav = document.getElementById('authNav');
    if (authNav) {
        authNav.innerHTML = `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                    <i class="fas fa-user"></i> ${user.firstName}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#"><i class="fas fa-user-circle"></i> الملف الشخصي</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout()"><i class="fas fa-sign-out-alt"></i> تسجيل الخروج</a></li>
                </ul>
            </li>
        `;
    }
}

// معالجة تسجيل الدخول
function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // البحث عن المستخدم في localStorage
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find(u => u.email === email && u.password === password);
    
    if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        showAlert('success', 'تم تسجيل الدخول بنجاح!');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    } else {
        showAlert('danger', 'البريد الإلكتروني أو كلمة المرور غير صحيحة');
    }
}

// معالجة التسجيل
function handleRegister(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const userType = document.getElementById('userType').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showAlert('danger', 'كلمات المرور غير متطابقة');
        return;
    }
    
    // التحقق من عدم وجود البريد الإلكتروني مسبقاً
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    if (users.some(u => u.email === email)) {
        showAlert('danger', 'البريد الإلكتروني مستخدم بالفعل');
        return;
    }
    
    // إنشاء مستخدم جديد
    const newUser = {
        firstName,
        lastName,
        email,
        phone,
        userType,
        password
    };
    
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    
    showAlert('success', 'تم إنشاء الحساب بنجاح!');
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 1500);
}

// تسجيل الخروج
function logout() {
    localStorage.removeItem('currentUser');
    showAlert('success', 'تم تسجيل الخروج بنجاح!');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1500);
}

// عرض رسائل التنبيه
function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer');
    if (alertContainer) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        alertContainer.appendChild(alert);
        
        // إخفاء التنبيه بعد 3 ثواني
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
}

// التحقق من حالة تسجيل الدخول عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});
