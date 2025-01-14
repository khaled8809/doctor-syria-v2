from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_otp import devices
from django_otp.plugins.otp_totp.models import TOTPDevice


class TwoFactorAuth:
    @staticmethod
    def setup_2fa(user):
        """إعداد المصادقة الثنائية للمستخدم"""
        try:
            # إزالة أي أجهزة سابقة
            TOTPDevice.objects.filter(user=user).delete()
            # إنشاء جهاز جديد
            device = TOTPDevice.objects.create(
                user=user, name=f"Default device for {user.username}", confirmed=False
            )
            return {"config_url": device.config_url(), "key": device.key.hex()}
        except Exception as e:
            raise Exception(f"Error setting up 2FA: {str(e)}")

    @staticmethod
    def verify_2fa(user, token):
        """التحقق من رمز المصادقة الثنائية"""
        try:
            device = TOTPDevice.objects.get(user=user)
            return device.verify_token(token)
        except ObjectDoesNotExist:
            return False
        except Exception as e:
            raise Exception(f"Error verifying 2FA: {str(e)}")
