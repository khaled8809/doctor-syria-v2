import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router basename="/doctor-syria-v2">
      <div className="app">
        <nav className="navbar">
          <div className="container">
            <Link to="/" className="navbar-brand">
              <i className="fas fa-hospital-alt"></i> Doctor Syria
            </Link>
            <div className="nav-links">
              <Link to="/about" className="nav-link">عن المشروع</Link>
              <Link to="/features" className="nav-link">المميزات</Link>
              <Link to="/docs" className="nav-link">الوثائق</Link>
              <a href="https://github.com/khaled8809/doctor-syria-v2" 
                 className="nav-link btn btn-outline-light btn-sm">
                <i className="fab fa-github"></i> GitHub
              </a>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/features" element={<Features />} />
            <Route path="/docs" element={<Documentation />} />
          </Routes>
        </main>

        <footer className="footer">
          <div className="container">
            <div className="footer-content">
              <div className="footer-section">
                <h3>Doctor Syria</h3>
                <p>نظام إدارة المستشفيات والعيادات الطبية المفتوح المصدر</p>
                <div className="social-links">
                  <a href="https://github.com/khaled8809/doctor-syria-v2" 
                     target="_blank" rel="noopener noreferrer">
                    <i className="fab fa-github"></i>
                  </a>
                  <a href="https://hub.docker.com/r/khaledmashoor/doctor-syria" 
                     target="_blank" rel="noopener noreferrer">
                    <i className="fab fa-docker"></i>
                  </a>
                </div>
              </div>
              <div className="footer-section">
                <h3>روابط سريعة</h3>
                <ul>
                  <li><Link to="/about">عن المشروع</Link></li>
                  <li><Link to="/features">المميزات</Link></li>
                  <li><Link to="/docs">الوثائق</Link></li>
                  <li><a href="https://github.com/khaled8809/doctor-syria-v2/issues">الدعم الفني</a></li>
                </ul>
              </div>
              <div className="footer-section">
                <h3>تواصل معنا</h3>
                <ul className="contact-info">
                  <li>
                    <i className="fas fa-envelope"></i>
                    <a href="mailto:support@doctor-syria.com">support@doctor-syria.com</a>
                  </li>
                  <li>
                    <i className="fab fa-github"></i>
                    <a href="https://github.com/khaled8809/doctor-syria-v2">GitHub</a>
                  </li>
                </ul>
              </div>
            </div>
            <div className="footer-bottom">
              <p>&copy; 2025 Doctor Syria. جميع الحقوق محفوظة</p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <>
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1>Doctor Syria</h1>
            <p className="lead">نظام شامل ومتكامل لإدارة المستشفيات والعيادات الطبية</p>
            <div className="cta-buttons">
              <a href="https://github.com/khaled8809/doctor-syria-v2" 
                 className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-github"></i> ابدأ الآن
              </a>
              <a href="https://hub.docker.com/r/khaledmashoor/doctor-syria" 
                 className="btn btn-outline" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-docker"></i> Docker Hub
              </a>
            </div>
          </div>
        </div>
        <div className="hero-waves">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
            <path fill="#ffffff" fillOpacity="1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,165.3C1248,149,1344,107,1392,85.3L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
          </svg>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2 className="section-title">المميزات الرئيسية</h2>
          <div className="features-grid">
            <div className="feature-card">
              <i className="fas fa-hospital-user"></i>
              <h3>إدارة المرضى</h3>
              <p>نظام متكامل لإدارة المرضى والمواعيد والسجلات الطبية</p>
              <Link to="/features" className="feature-link">اكتشف المزيد</Link>
            </div>
            <div className="feature-card">
              <i className="fas fa-flask"></i>
              <h3>المختبر والصيدلية</h3>
              <p>إدارة متقدمة للتحاليل المخبرية والأدوية</p>
              <Link to="/features" className="feature-link">اكتشف المزيد</Link>
            </div>
            <div className="feature-card">
              <i className="fas fa-file-invoice-dollar"></i>
              <h3>إدارة الفواتير</h3>
              <p>نظام فوترة متكامل مع تقارير مالية تفصيلية</p>
              <Link to="/features" className="feature-link">اكتشف المزيد</Link>
            </div>
          </div>
        </div>
      </section>

      <section className="tech-stack">
        <div className="container">
          <h2 className="section-title">التقنيات المستخدمة</h2>
          <div className="tech-grid">
            <div className="tech-item">
              <i className="fab fa-python"></i>
              <h4>Django</h4>
            </div>
            <div className="tech-item">
              <i className="fab fa-react"></i>
              <h4>React</h4>
            </div>
            <div className="tech-item">
              <i className="fab fa-docker"></i>
              <h4>Docker</h4>
            </div>
            <div className="tech-item">
              <i className="fas fa-database"></i>
              <h4>PostgreSQL</h4>
            </div>
          </div>
        </div>
      </section>

      <section className="stats">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">+1000</div>
              <div className="stat-label">مستشفى وعيادة</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">+5000</div>
              <div className="stat-label">طبيب</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">+50000</div>
              <div className="stat-label">مريض</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">دعم فني</div>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>ابدأ باستخدام Doctor Syria اليوم</h2>
          <p>انضم إلى مجتمعنا المتنامي من المستشفيات والعيادات</p>
          <div className="cta-buttons">
            <a href="https://github.com/khaled8809/doctor-syria-v2" 
               className="btn btn-primary" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-github"></i> ابدأ الآن
            </a>
            <Link to="/docs" className="btn btn-outline">
              <i className="fas fa-book"></i> تصفح الوثائق
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}

function About() {
  return (
    <section className="about">
      <div className="container">
        <h2 className="section-title">عن المشروع</h2>
        <div className="about-content">
          <div className="about-text">
            <p className="lead">
              Doctor Syria هو نظام إدارة مستشفيات مفتوح المصدر يهدف إلى تسهيل وتحسين
              إدارة المرافق الطبية في سوريا.
            </p>
            <p>
              يوفر النظام حلاً شاملاً لجميع احتياجات المستشفيات والعيادات، بما في ذلك:
            </p>
            <ul className="about-features">
              <li>إدارة المرضى والمواعيد</li>
              <li>السجلات الطبية الإلكترونية</li>
              <li>إدارة المختبر والصيدلية</li>
              <li>نظام الفوترة والتأمين</li>
              <li>التقارير والإحصائيات</li>
            </ul>
          </div>
          <div className="about-image">
            <img src="/doctor-syria-v2/images/about.jpg" alt="Doctor Syria Dashboard" />
          </div>
        </div>
      </div>
    </section>
  );
}

function Features() {
  return (
    <section className="features-page">
      <div className="container">
        <h2 className="section-title">المميزات</h2>
        <div className="features-list">
          <div className="feature-item">
            <i className="fas fa-user-md"></i>
            <h3>إدارة المرضى</h3>
            <ul>
              <li>سجلات المرضى الإلكترونية</li>
              <li>جدولة المواعيد</li>
              <li>التاريخ الطبي</li>
              <li>متابعة الحالات</li>
            </ul>
          </div>
          <div className="feature-item">
            <i className="fas fa-flask"></i>
            <h3>المختبر</h3>
            <ul>
              <li>إدارة التحاليل</li>
              <li>النتائج والتقارير</li>
              <li>المتابعة المخبرية</li>
              <li>إحصائيات المختبر</li>
            </ul>
          </div>
          <div className="feature-item">
            <i className="fas fa-pills"></i>
            <h3>الصيدلية</h3>
            <ul>
              <li>إدارة المخزون</li>
              <li>الوصفات الطبية</li>
              <li>تتبع الأدوية</li>
              <li>التنبيهات التلقائية</li>
            </ul>
          </div>
          <div className="feature-item">
            <i className="fas fa-chart-line"></i>
            <h3>التقارير</h3>
            <ul>
              <li>تقارير مالية</li>
              <li>إحصائيات المرضى</li>
              <li>تقارير الأداء</li>
              <li>تحليلات البيانات</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

function Documentation() {
  return (
    <section className="documentation">
      <div className="container">
        <h2 className="section-title">الوثائق</h2>
        <div className="docs-grid">
          <a href="https://github.com/khaled8809/doctor-syria-v2#readme" 
             className="doc-card" target="_blank" rel="noopener noreferrer">
            <i className="fas fa-book"></i>
            <h3>دليل المستخدم</h3>
            <p>تعلم كيفية استخدام النظام خطوة بخطوة</p>
          </a>
          <a href="https://github.com/khaled8809/doctor-syria-v2/wiki" 
             className="doc-card" target="_blank" rel="noopener noreferrer">
            <i className="fas fa-graduation-cap"></i>
            <h3>الوثائق التقنية</h3>
            <p>معلومات تقنية مفصلة للمطورين</p>
          </a>
          <a href="https://sonarcloud.io/project/overview?id=khaled8809_doctor-syria-v2" 
             className="doc-card" target="_blank" rel="noopener noreferrer">
            <i className="fas fa-chart-line"></i>
            <h3>تقارير الجودة</h3>
            <p>تحليلات وتقارير جودة الكود</p>
          </a>
        </div>
      </div>
    </section>
  );
}

export default App;
