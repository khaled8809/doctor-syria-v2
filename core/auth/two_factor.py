import pyotp
import qrcode
from io import BytesIO
import base64
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

class TwoFactorAuth:
    """
    Handle two-factor authentication using TOTP (Time-based One-Time Password)
    """
    
    @staticmethod
    def generate_totp_secret():
        """Generate a new TOTP secret"""
        return pyotp.random_base32()

    @staticmethod
    def get_totp_uri(secret: str, username: str) -> str:
        """Generate the TOTP URI for QR code generation"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=username,
            issuer_name=settings.TWO_FACTOR_ISSUER_NAME
        )

    @staticmethod
    def generate_qr_code(uri: str) -> str:
        """Generate QR code image as base64 string"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """Verify a TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)

    @staticmethod
    def generate_backup_codes() -> list:
        """Generate backup codes for account recovery"""
        return [pyotp.random_base32()[:8] for _ in range(8)]

    @staticmethod
    def store_temp_secret(user_id: int, secret: str, timeout: int = 300):
        """Store temporary TOTP secret in cache during setup"""
        cache_key = f"2fa_setup_{user_id}"
        cache.set(cache_key, secret, timeout)

    @staticmethod
    def get_temp_secret(user_id: int) -> str:
        """Get temporary TOTP secret from cache"""
        cache_key = f"2fa_setup_{user_id}"
        return cache.get(cache_key)

    @staticmethod
    def clear_temp_secret(user_id: int):
        """Clear temporary TOTP secret from cache"""
        cache_key = f"2fa_setup_{user_id}"
        cache.delete(cache_key)

    @classmethod
    def setup_2fa(cls, user: User) -> dict:
        """Set up 2FA for a user"""
        secret = cls.generate_totp_secret()
        uri = cls.get_totp_uri(secret, user.username)
        qr_code = cls.generate_qr_code(uri)
        backup_codes = cls.generate_backup_codes()
        
        # Store temporary secret
        cls.store_temp_secret(user.id, secret)
        
        return {
            'secret': secret,
            'qr_code': qr_code,
            'backup_codes': backup_codes,
        }

    @classmethod
    def confirm_2fa_setup(cls, user: User, token: str) -> bool:
        """Confirm 2FA setup with a token"""
        secret = cls.get_temp_secret(user.id)
        if not secret:
            return False
            
        if cls.verify_totp(secret, token):
            # Save the secret to user's profile
            user.two_factor_secret = secret
            user.two_factor_enabled = True
            user.save()
            
            # Clear temporary secret
            cls.clear_temp_secret(user.id)
            return True
            
        return False

    @classmethod
    def disable_2fa(cls, user: User):
        """Disable 2FA for a user"""
        user.two_factor_secret = None
        user.two_factor_enabled = False
        user.save()
