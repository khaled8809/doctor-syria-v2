"""
اختبارات وحدة المصادقة البيومترية
Biometric Authentication Tests
"""

import json
from datetime import datetime

import numpy as np
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from doctor_syria.auth.biometric import BiometricManager

User = get_user_model()


@pytest.mark.django_db
class TestBiometric:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def test_user(self):
        return User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    @pytest.fixture
    def biometric_manager(self, test_user):
        return BiometricManager(test_user)

    def test_fingerprint_registration(self, biometric_manager):
        # Test successful registration
        fingerprint_data = "test_fingerprint_data"
        assert biometric_manager.register_fingerprint(fingerprint_data)

        # Verify fingerprint was stored
        assert hasattr(biometric_manager.user, "fingerprint_hash")
        assert hasattr(biometric_manager.user, "fingerprint_salt")

        # Test verification
        assert biometric_manager.verify_fingerprint(fingerprint_data)
        assert not biometric_manager.verify_fingerprint("wrong_data")

    def test_face_registration(self, biometric_manager):
        # Generate test face data
        face_data = "test_face_image"
        face_encoding = [0.1, 0.2, 0.3, 0.4]

        # Test registration
        assert biometric_manager.register_face(face_data, face_encoding)

        # Verify face data was stored
        assert hasattr(biometric_manager.user, "face_encoding")
        assert hasattr(biometric_manager.user, "face_data")

        # Test verification
        similar_encoding = [0.11, 0.21, 0.31, 0.41]  # Similar face
        different_encoding = [0.9, 0.8, 0.7, 0.6]  # Different face

        assert biometric_manager.verify_face(face_data, similar_encoding)
        assert not biometric_manager.verify_face(face_data, different_encoding)

    def test_voice_registration(self, biometric_manager):
        # Generate test voice data
        voice_data = "test_voice_recording"
        voice_features = [0.5, 0.6, 0.7, 0.8]

        # Test registration
        assert biometric_manager.register_voice(voice_data, voice_features)

        # Verify voice data was stored
        assert hasattr(biometric_manager.user, "voice_features")
        assert hasattr(biometric_manager.user, "voice_data")

        # Test verification
        similar_features = [0.51, 0.61, 0.71, 0.81]  # Similar voice
        different_features = [0.1, 0.2, 0.3, 0.4]  # Different voice

        assert biometric_manager.verify_voice(voice_data, similar_features)
        assert not biometric_manager.verify_voice(voice_data, different_features)

    def test_available_methods(self, biometric_manager):
        # Initially no methods available
        methods = biometric_manager.get_available_methods()
        assert not any(methods.values())

        # Register fingerprint
        biometric_manager.register_fingerprint("test_data")
        methods = biometric_manager.get_available_methods()
        assert methods["fingerprint"]
        assert not methods["face"]
        assert not methods["voice"]

        # Register face
        biometric_manager.register_face("test_data", [0.1, 0.2, 0.3])
        methods = biometric_manager.get_available_methods()
        assert methods["fingerprint"]
        assert methods["face"]
        assert not methods["voice"]

        # Register voice
        biometric_manager.register_voice("test_data", [0.4, 0.5, 0.6])
        methods = biometric_manager.get_available_methods()
        assert all(methods.values())

    def test_clear_biometric_data(self, biometric_manager):
        # Register all biometric data
        biometric_manager.register_fingerprint("test_fingerprint")
        biometric_manager.register_face("test_face", [0.1, 0.2])
        biometric_manager.register_voice("test_voice", [0.3, 0.4])

        # Verify data exists
        methods = biometric_manager.get_available_methods()
        assert all(methods.values())

        # Clear data
        assert biometric_manager.clear_biometric_data()

        # Verify data was cleared
        methods = biometric_manager.get_available_methods()
        assert not any(methods.values())

    def test_error_handling(self, biometric_manager):
        # Test invalid fingerprint data
        assert not biometric_manager.verify_fingerprint(None)

        # Test invalid face data
        assert not biometric_manager.verify_face(None, None)

        # Test invalid voice data
        assert not biometric_manager.verify_voice(None, None)
