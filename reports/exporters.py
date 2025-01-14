"""
خدمات تصدير التقارير
"""

import csv
import json
import os
from datetime import datetime

import xlsxwriter
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import MedicalReport, StatisticalReport


class ReportExporter:
    """مصدّر التقارير بتنسيقات مختلفة"""

    EXPORT_FORMATS = ["pdf", "excel", "csv", "json"]

    def __init__(self, report_data, report_type, template_name=None):
        self.report_data = report_data
        self.report_type = report_type
        self.template_name = template_name or f"reports/{report_type}_report.html"
        self.export_dir = os.path.join(settings.MEDIA_ROOT, "exports", "reports")
        os.makedirs(self.export_dir, exist_ok=True)

    def export(self, format_type):
        """تصدير التقرير بالتنسيق المطلوب"""
        if format_type not in self.EXPORT_FORMATS:
            raise ValueError(
                f"تنسيق غير مدعوم. التنسيقات المدعومة: {', '.join(self.EXPORT_FORMATS)}"
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_type}_{timestamp}"

        if format_type == "pdf":
            return self._export_pdf(filename)
        elif format_type == "excel":
            return self._export_excel(filename)
        elif format_type == "csv":
            return self._export_csv(filename)
        elif format_type == "json":
            return self._export_json(filename)

    def _export_pdf(self, filename):
        """تصدير إلى PDF"""
        output_file = os.path.join(self.export_dir, f"{filename}.pdf")

        # تحضير قالب HTML
        html_content = render_to_string(
            self.template_name,
            {
                "report": self.report_data,
                "generated_at": datetime.now(),
            },
        )

        # إنشاء PDF
        HTML(string=html_content).write_pdf(
            output_file,
            stylesheets=[os.path.join(settings.STATIC_ROOT, "css/report_pdf.css")],
        )

        return output_file

    def _export_excel(self, filename):
        """تصدير إلى Excel"""
        output_file = os.path.join(self.export_dir, f"{filename}.xlsx")
        workbook = xlsxwriter.Workbook(output_file)

        # تنسيقات الخلايا
        header_format = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "bg_color": "#4CAF50",
                "font_color": "white",
            }
        )

        date_format = workbook.add_format({"num_format": "yyyy-mm-dd"})
        number_format = workbook.add_format({"num_format": "#,##0.00"})

        # إنشاء ورقة البيانات الرئيسية
        worksheet = workbook.add_worksheet("البيانات الرئيسية")

        # كتابة البيانات حسب نوع التقرير
        if isinstance(self.report_data, dict):
            row = 0
            for key, value in self.report_data.items():
                worksheet.write(row, 0, key, header_format)
                if isinstance(value, (list, dict)):
                    worksheet.write(row, 1, json.dumps(value, ensure_ascii=False))
                else:
                    worksheet.write(row, 1, value)
                row += 1
        elif isinstance(self.report_data, list):
            if self.report_data:
                headers = list(self.report_data[0].keys())
                for col, header in enumerate(headers):
                    worksheet.write(0, col, header, header_format)

                for row, data in enumerate(self.report_data, start=1):
                    for col, header in enumerate(headers):
                        value = data[header]
                        if isinstance(value, datetime):
                            worksheet.write(row, col, value, date_format)
                        elif isinstance(value, (int, float)):
                            worksheet.write(row, col, value, number_format)
                        else:
                            worksheet.write(row, col, value)

        workbook.close()
        return output_file

    def _export_csv(self, filename):
        """تصدير إلى CSV"""
        output_file = os.path.join(self.export_dir, f"{filename}.csv")

        with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
            if isinstance(self.report_data, dict):
                writer = csv.writer(csvfile)
                writer.writerow(["المفتاح", "القيمة"])
                for key, value in self.report_data.items():
                    writer.writerow(
                        [
                            key,
                            (
                                json.dumps(value, ensure_ascii=False)
                                if isinstance(value, (list, dict))
                                else value
                            ),
                        ]
                    )
            elif isinstance(self.report_data, list):
                if self.report_data:
                    writer = csv.DictWriter(
                        csvfile, fieldnames=self.report_data[0].keys()
                    )
                    writer.writeheader()
                    writer.writerows(self.report_data)

        return output_file

    def _export_json(self, filename):
        """تصدير إلى JSON"""
        output_file = os.path.join(self.export_dir, f"{filename}.json")

        with open(output_file, "w", encoding="utf-8") as jsonfile:
            json.dump(self.report_data, jsonfile, ensure_ascii=False, indent=2)

        return output_file


class MedicalReportExporter(ReportExporter):
    """مصدّر التقارير الطبية"""

    def __init__(self, medical_report):
        super().__init__(
            self._prepare_report_data(medical_report),
            "medical",
            "reports/medical_report.html",
        )

    def _prepare_report_data(self, report):
        """تحضير بيانات التقرير الطبي"""
        return {
            "report_info": {
                "id": report.id,
                "type": report.get_report_type_display(),
                "title": report.title,
                "created_at": report.created_at.isoformat(),
            },
            "patient_info": {
                "name": report.patient.full_name,
                "id": report.patient.id,
                "age": report.patient.age,
                "gender": report.patient.gender,
            },
            "medical_info": {
                "diagnosis": report.diagnosis,
                "treatment_plan": report.treatment_plan,
                "medications": report.medications,
            },
            "content": report.content,
            "attachments": report.attachments,
        }


class StatisticalReportExporter(ReportExporter):
    """مصدّر التقارير الإحصائية"""

    def __init__(self, statistical_report):
        super().__init__(
            self._prepare_report_data(statistical_report),
            "statistical",
            "reports/statistical_report.html",
        )

    def _prepare_report_data(self, report):
        """تحضير بيانات التقرير الإحصائي"""
        return {
            "report_info": {
                "id": report.id,
                "title": report.title,
                "period": report.get_period_display(),
                "start_date": report.start_date.isoformat(),
                "end_date": report.end_date.isoformat(),
                "created_at": report.created_at.isoformat(),
            },
            "summary": report.summary,
            "data": report.data,
            "categories": report.categories,
            "visualization_settings": report.visualization_settings,
        }
