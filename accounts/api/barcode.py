"""
API endpoints للتعامل مع الباركود والبطاقات التعريفية
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from accounts.models import User
from accounts.utils.id_card_generator import IDCardGenerator
import json

class BarcodeScannerView(APIView):
    """API view لمسح الباركود"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """معالجة الباركود الممسوح"""
        try:
            barcode_data = request.data.get('barcode')
            if not barcode_data:
                return Response({
                    'success': False,
                    'error': 'لم يتم توفير بيانات الباركود'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # تحويل البيانات من نص إلى كائن
            data = json.loads(barcode_data.replace("'", '"'))
            
            # البحث عن المستخدم
            user = get_object_or_404(User, id=data['id'])
            
            # التحقق من صحة البيانات
            if (user.username != data['username'] or 
                user.role != data['role'] or 
                user.created_at.isoformat() != data['created_at']):
                raise ValueError('بيانات الباركود غير صالحة')
            
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.get_full_name(),
                    'role': user.get_role(),
                    'email': user.email
                }
            })
            
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'المستخدم غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except (json.JSONDecodeError, ValueError) as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'حدث خطأ أثناء معالجة الباركود'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegenerateIDCardView(APIView):
    """API view لإعادة توليد البطاقة التعريفية"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """إعادة توليد البطاقة التعريفية للمستخدم الحالي"""
        try:
            user = request.user
            generator = IDCardGenerator()
            id_card_path = generator.create_card(user)
            
            # تحديث مسار البطاقة في نموذج المستخدم
            user.id_card = id_card_path
            user.save(update_fields=['id_card'])
            
            return Response({
                'success': True,
                'id_card_url': user.get_id_card_url()
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'حدث خطأ أثناء إعادة توليد البطاقة'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
