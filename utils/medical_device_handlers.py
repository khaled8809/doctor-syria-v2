"""
وحدة معالجة الأخطاء للأجهزة الطبية
"""

import logging
from typing import Any, Dict, Optional

from pydicom.dataset import Dataset
from pynetdicom import AE
from pynetdicom.status import code_to_category

logger = logging.getLogger(__name__)


class MedicalDeviceError(Exception):
    """فئة مخصصة لأخطاء الأجهزة الطبية"""

    pass


class DicomConnectionHandler:
    """معالج اتصالات DICOM"""

    def __init__(self, host: str, port: int, ae_title: str):
        self.host = host
        self.port = port
        self.ae_title = ae_title
        self.ae = AE(ae_title=ae_title)

    def connect(self) -> bool:
        """إنشاء اتصال مع جهاز DICOM"""
        try:
            assoc = self.ae.associate(self.host, self.port)
            if assoc.is_established:
                logger.info(f"تم الاتصال بنجاح مع {self.ae_title}")
                assoc.release()
                return True
            else:
                logger.error(f"فشل الاتصال مع {self.ae_title}")
                return False
        except Exception as e:
            logger.error(f"خطأ في الاتصال: {str(e)}")
            raise MedicalDeviceError(f"فشل الاتصال مع الجهاز: {str(e)}")


class HL7MessageHandler:
    """معالج رسائل HL7"""

    @staticmethod
    def validate_message(message: str) -> bool:
        """التحقق من صحة رسالة HL7"""
        try:
            segments = message.split("\r")
            if not segments[0].startswith("MSH"):
                logger.error("رسالة HL7 غير صالحة: لا يوجد قطاع MSH")
                return False
            return True
        except Exception as e:
            logger.error(f"خطأ في التحقق من رسالة HL7: {str(e)}")
            return False

    @staticmethod
    def parse_message(message: str) -> Dict[str, Any]:
        """تحليل رسالة HL7"""
        try:
            result = {}
            segments = message.split("\r")
            for segment in segments:
                fields = segment.split("|")
                result[fields[0]] = fields[1:]
            return result
        except Exception as e:
            logger.error(f"خطأ في تحليل رسالة HL7: {str(e)}")
            raise MedicalDeviceError(f"فشل تحليل رسالة HL7: {str(e)}")


def handle_device_error(error: Exception) -> Dict[str, str]:
    """معالجة الأخطاء العامة للأجهزة"""
    error_message = str(error)
    error_type = type(error).__name__

    logger.error(f"نوع الخطأ: {error_type}, الرسالة: {error_message}")

    return {
        "error_type": error_type,
        "error_message": error_message,
        "recommendation": get_error_recommendation(error_type),
    }


def get_error_recommendation(error_type: str) -> str:
    """الحصول على توصيات لحل المشكلة"""
    recommendations = {
        "ConnectionError": "تحقق من اتصال الشبكة وتأكد من أن الجهاز متصل ويعمل",
        "TimeoutError": "حاول مرة أخرى، قد يكون الجهاز مشغولاً أو بطيئاً",
        "MedicalDeviceError": "راجع سجلات الأخطاء للحصول على مزيد من التفاصيل",
        "ValueError": "تحقق من صحة البيانات المدخلة",
    }
    return recommendations.get(error_type, "اتصل بالدعم الفني للمساعدة")
