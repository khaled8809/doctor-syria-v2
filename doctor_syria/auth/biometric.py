"""
وحدة المصادقة البيومترية
Biometric Authentication Module

This module handles biometric authentication including:
- Fingerprint verification
- Face recognition
- Voice recognition
"""

import base64
import hashlib
import hmac
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger("auth.biometric")


class BiometricManager:
    """
    إدارة المصادقة البيومترية
    Biometric Authentication Manager
    """

    def __init__(self, user: Any):
        self.user = user

    def register_fingerprint(self, fingerprint_data: str) -> bool:
        """
        تسجيل بصمة الإصبع
        Register fingerprint

        Args:
            fingerprint_data: بيانات البصمة | Fingerprint data

        Returns:
            bool: True if registration successful
        """
        try:
            # Hash the fingerprint data for secure storage
            salt = hashlib.sha256(str(datetime.now()).encode()).hexdigest()
            fingerprint_hash = hashlib.pbkdf2_hmac(
                "sha256", fingerprint_data.encode(), salt.encode(), 100000
            ).hex()

            self.user.fingerprint_hash = fingerprint_hash
            self.user.fingerprint_salt = salt
            self.user.save()

            logger.info(f"Fingerprint registered for user {self.user.email}")
            return True

        except Exception as e:
            logger.error(
                f"Fingerprint registration error for user {self.user.email}: {e}"
            )
            return False

    def verify_fingerprint(self, fingerprint_data: str) -> bool:
        """
        التحقق من بصمة الإصبع
        Verify fingerprint

        Args:
            fingerprint_data: بيانات البصمة | Fingerprint data

        Returns:
            bool: True if fingerprint is valid
        """
        try:
            if not hasattr(self.user, "fingerprint_hash"):
                return False

            test_hash = hashlib.pbkdf2_hmac(
                "sha256",
                fingerprint_data.encode(),
                self.user.fingerprint_salt.encode(),
                100000,
            ).hex()

            return hmac.compare_digest(
                test_hash.encode(), self.user.fingerprint_hash.encode()
            )

        except Exception as e:
            logger.error(
                f"Fingerprint verification error for user {self.user.email}: {e}"
            )
            return False

    def register_face(self, face_data: str, face_encoding: list) -> bool:
        """
        تسجيل الوجه
        Register face

        Args:
            face_data: صورة الوجه | Face image data
            face_encoding: ترميز الوجه | Face encoding

        Returns:
            bool: True if registration successful
        """
        try:
            face_info = {
                "encoding": face_encoding,
                "timestamp": datetime.now().isoformat(),
            }

            self.user.face_encoding = json.dumps(face_info)
            self.user.face_data = face_data
            self.user.save()

            logger.info(f"Face registered for user {self.user.email}")
            return True

        except Exception as e:
            logger.error(f"Face registration error for user {self.user.email}: {e}")
            return False

    def verify_face(
        self, face_data: str, face_encoding: list, threshold: float = 0.6
    ) -> bool:
        """
        التحقق من الوجه
        Verify face

        Args:
            face_data: صورة الوجه | Face image data
            face_encoding: ترميز الوجه | Face encoding
            threshold: عتبة التطابق | Matching threshold

        Returns:
            bool: True if face is valid
        """
        try:
            if not hasattr(self.user, "face_encoding"):
                return False

            stored_face = json.loads(self.user.face_encoding)
            stored_encoding = stored_face["encoding"]

            # Calculate face distance
            import numpy as np

            distance = np.linalg.norm(
                np.array(face_encoding) - np.array(stored_encoding)
            )

            return distance < threshold

        except Exception as e:
            logger.error(f"Face verification error for user {self.user.email}: {e}")
            return False

    def register_voice(self, voice_data: str, voice_features: list) -> bool:
        """
        تسجيل الصوت
        Register voice

        Args:
            voice_data: بيانات الصوت | Voice data
            voice_features: ميزات الصوت | Voice features

        Returns:
            bool: True if registration successful
        """
        try:
            voice_info = {
                "features": voice_features,
                "timestamp": datetime.now().isoformat(),
            }

            self.user.voice_features = json.dumps(voice_info)
            self.user.voice_data = voice_data
            self.user.save()

            logger.info(f"Voice registered for user {self.user.email}")
            return True

        except Exception as e:
            logger.error(f"Voice registration error for user {self.user.email}: {e}")
            return False

    def verify_voice(
        self, voice_data: str, voice_features: list, threshold: float = 0.7
    ) -> bool:
        """
        التحقق من الصوت
        Verify voice

        Args:
            voice_data: بيانات الصوت | Voice data
            voice_features: ميزات الصوت | Voice features
            threshold: عتبة التطابق | Matching threshold

        Returns:
            bool: True if voice is valid
        """
        try:
            if not hasattr(self.user, "voice_features"):
                return False

            stored_voice = json.loads(self.user.voice_features)
            stored_features = stored_voice["features"]

            # Calculate voice similarity
            import numpy as np

            similarity = np.dot(np.array(voice_features), np.array(stored_features)) / (
                np.linalg.norm(voice_features) * np.linalg.norm(stored_features)
            )

            return similarity > threshold

        except Exception as e:
            logger.error(f"Voice verification error for user {self.user.email}: {e}")
            return False

    def get_available_methods(self) -> Dict[str, bool]:
        """
        الحصول على طرق المصادقة المتاحة
        Get available biometric methods

        Returns:
            Dict[str, bool]: Available methods
        """
        return {
            "fingerprint": hasattr(self.user, "fingerprint_hash"),
            "face": hasattr(self.user, "face_encoding"),
            "voice": hasattr(self.user, "voice_features"),
        }

    def clear_biometric_data(self) -> bool:
        """
        مسح بيانات المصادقة البيومترية
        Clear all biometric data

        Returns:
            bool: True if data was cleared successfully
        """
        try:
            for attr in [
                "fingerprint_hash",
                "fingerprint_salt",
                "face_encoding",
                "face_data",
                "voice_features",
                "voice_data",
            ]:
                if hasattr(self.user, attr):
                    setattr(self.user, attr, None)

            self.user.save()
            logger.info(f"Biometric data cleared for user {self.user.email}")
            return True

        except Exception as e:
            logger.error(
                f"Error clearing biometric data for user {self.user.email}: {e}"
            )
            return False
