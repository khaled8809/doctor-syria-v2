"""
API endpoints للتعامل مع الباركود والبطاقات التعريفية
"""

import json
import logging

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.utils.id_card_generator import IDCardGenerationError, IDCardGenerator

logger = logging.getLogger(__name__)


class InvalidBarcodeDataError(Exception):
    """استثناء مخصص لبيانات الباركود غير الصالحة"""

    pass


class BarcodeScannerView(APIView):
    """API view لمسح الباركود"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """معالجة الباركود الممسوح"""
        try:
            barcode_data = request.data.get("barcode")
            if not barcode_data:
                return Response(
                    {
                        "success": False,
                        "error": "لم يتم توفير بيانات الباركود",
                        "error_code": "MISSING_BARCODE_DATA",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # تحويل البيانات من نص إلى كائن
            try:
                data = json.loads(barcode_data.replace("'", '"'))
            except json.JSONDecodeError:
                raise InvalidBarcodeDataError(
                    "بيانات الباركود غير صالحة: تنسيق JSON غير صحيح"
                )

            # التحقق من وجود الحقول المطلوبة
            required_fields = ["id", "username", "role", "created_at"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise InvalidBarcodeDataError(
                    f'بيانات الباركود غير مكتملة. الحقول المفقودة: {", ".join(missing_fields)}'
                )

            # البحث عن المستخدم
            try:
                user = User.objects.get(id=data["id"])
            except (User.DoesNotExist, ValueError):
                return Response(
                    {
                        "success": False,
                        "error": "المستخدم غير موجود",
                        "error_code": "USER_NOT_FOUND",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # التحقق من صحة البيانات
            if (
                user.username != data["username"]
                or user.role != data["role"]
                or user.created_at.isoformat() != data["created_at"]
            ):
                raise InvalidBarcodeDataError(
                    "بيانات الباركود لا تتطابق مع بيانات المستخدم"
                )

            # تسجيل نجاح العملية
            logger.info(f"تم مسح باركود المستخدم بنجاح: {user.username}")

            return Response(
                {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.get_full_name(),
                        "role": user.get_role(),
                        "email": user.email,
                    },
                }
            )

        except InvalidBarcodeDataError as e:
            logger.warning(f"خطأ في بيانات الباركود: {str(e)}")
            return Response(
                {
                    "success": False,
                    "error": str(e),
                    "error_code": "INVALID_BARCODE_DATA",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"خطأ غير متوقع في معالجة الباركود: {str(e)}")
            return Response(
                {
                    "success": False,
                    "error": "حدث خطأ أثناء معالجة الباركود",
                    "error_code": "INTERNAL_ERROR",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RegenerateIDCardView(APIView):
    """API view لإعادة توليد البطاقة التعريفية"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """إعادة توليد البطاقة التعريفية للمستخدم الحالي"""
        try:
            user = request.user
            generator = IDCardGenerator()

            # التحقق من صلاحية بيانات المستخدم
            if not user.is_profile_complete():
                raise ValidationError(
                    "يجب إكمال الملف الشخصي قبل توليد البطاقة التعريفية"
                )

            # توليد البطاقة
            id_card_path = generator.create_card(user)

            # تحديث مسار البطاقة في نموذج المستخدم
            user.id_card = id_card_path
            user.save(update_fields=["id_card"])

            # تسجيل نجاح العملية
            logger.info(f"تم إعادة توليد البطاقة التعريفية للمستخدم: {user.username}")

            return Response({"success": True, "id_card_url": user.get_id_card_url()})

        except ValidationError as e:
            logger.warning(f"خطأ في بيانات المستخدم: {str(e)}")
            return Response(
                {"success": False, "error": str(e), "error_code": "INVALID_USER_DATA"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except IDCardGenerationError as e:
            logger.error(f"خطأ في توليد البطاقة التعريفية: {str(e)}")
            return Response(
                {
                    "success": False,
                    "error": str(e),
                    "error_code": "CARD_GENERATION_ERROR",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            logger.error(f"خطأ غير متوقع في توليد البطاقة التعريفية: {str(e)}")
            return Response(
                {
                    "success": False,
                    "error": "حدث خطأ أثناء توليد البطاقة التعريفية",
                    "error_code": "INTERNAL_ERROR",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
