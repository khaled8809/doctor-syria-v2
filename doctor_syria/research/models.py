from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Doctor, Hospital, Patient


class ResearchProject(models.Model):
    """المشاريع البحثية"""

    STATUS_CHOICES = [
        ("planning", "تخطيط"),
        ("recruiting", "توظيف"),
        ("active", "نشط"),
        ("analysis", "تحليل"),
        ("writing", "كتابة"),
        ("review", "مراجعة"),
        ("published", "منشور"),
        ("completed", "مكتمل"),
        ("suspended", "معلق"),
        ("terminated", "منتهي"),
    ]

    STUDY_TYPES = [
        ("observational", "دراسة ملاحظة"),
        ("interventional", "دراسة تدخلية"),
        ("clinical_trial", "تجربة سريرية"),
        ("survey", "استبيان"),
        ("case_study", "دراسة حالة"),
        ("meta_analysis", "تحليل تلوي"),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    principal_investigator = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="led_projects"
    )
    co_investigators = models.ManyToManyField(Doctor, related_name="research_projects")
    institution = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    study_type = models.CharField(max_length=20, choices=STUDY_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    objectives = models.TextField()
    methodology = models.TextField()
    inclusion_criteria = models.JSONField()
    exclusion_criteria = models.JSONField()
    target_sample_size = models.PositiveIntegerField()
    current_sample_size = models.PositiveIntegerField(default=0)
    funding_source = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    ethical_approval = models.BooleanField(default=False)
    approval_document = models.FileField(
        upload_to="research_approvals/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Participant(models.Model):
    """المشاركون في البحث"""

    STATUS_CHOICES = [
        ("screening", "فحص"),
        ("enrolled", "مسجل"),
        ("active", "نشط"),
        ("completed", "مكتمل"),
        ("withdrawn", "منسحب"),
        ("excluded", "مستبعد"),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    group_assignment = models.CharField(max_length=100, blank=True)
    consent_form = models.FileField(upload_to="research_consents/")
    withdrawal_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.project.title}"


class DataCollection(models.Model):
    """جمع البيانات"""

    DATA_TYPES = [
        ("survey", "استبيان"),
        ("measurement", "قياس"),
        ("lab_result", "نتيجة مخبرية"),
        ("observation", "ملاحظة"),
        ("interview", "مقابلة"),
        ("medical_record", "سجل طبي"),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    collection_date = models.DateTimeField()
    collected_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    data = models.JSONField()
    files = models.FileField(upload_to="research_data/", null=True, blank=True)
    validated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_data_type_display()} - {self.participant}"


class Analysis(models.Model):
    """التحليل الإحصائي"""

    ANALYSIS_TYPES = [
        ("descriptive", "وصفي"),
        ("inferential", "استدلالي"),
        ("regression", "انحدار"),
        ("correlation", "ارتباط"),
        ("survival", "بقاء"),
        ("machine_learning", "تعلم آلي"),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    description = models.TextField()
    methodology = models.TextField()
    results = models.JSONField()
    interpretation = models.TextField()
    performed_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    performed_at = models.DateTimeField()
    software_used = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    files = models.FileField(upload_to="research_analysis/", null=True, blank=True)

    def __str__(self):
        return f"{self.get_analysis_type_display()} - {self.project.title}"

    class Meta:
        verbose_name_plural = "Analyses"


class Publication(models.Model):
    """المنشورات"""

    PUBLICATION_TYPES = [
        ("journal_article", "مقال مجلة"),
        ("conference_paper", "ورقة مؤتمر"),
        ("poster", "ملصق"),
        ("thesis", "أطروحة"),
        ("report", "تقرير"),
    ]

    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("submitted", "مقدم"),
        ("under_review", "قيد المراجعة"),
        ("revision", "تعديل"),
        ("accepted", "مقبول"),
        ("published", "منشور"),
        ("rejected", "مرفوض"),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField("accounts.User")
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES)
    journal_name = models.CharField(max_length=200, blank=True)
    conference_name = models.CharField(max_length=200, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    acceptance_date = models.DateField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    abstract = models.TextField()
    keywords = models.JSONField(default=list)
    file = models.FileField(upload_to="research_publications/", null=True, blank=True)

    def __str__(self):
        return self.title


class Grant(models.Model):
    """المنح البحثية"""

    STATUS_CHOICES = [
        ("draft", "مسودة"),
        ("submitted", "مقدم"),
        ("under_review", "قيد المراجعة"),
        ("approved", "موافق عليه"),
        ("rejected", "مرفوض"),
        ("active", "نشط"),
        ("completed", "مكتمل"),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    funding_agency = models.CharField(max_length=200)
    grant_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    proposal = models.FileField(upload_to="research_grants/")
    budget_breakdown = models.JSONField()
    reports_required = models.JSONField(default=list)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.funding_agency} - {self.grant_number}"


class ResearchCollaboration(models.Model):
    """التعاون البحثي"""

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    agreement_file = models.FileField(upload_to="research_collaborations/")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.institution} - {self.project.title}"
