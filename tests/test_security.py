"""
Security tests for Doctor Syria Platform.
"""

import pytest
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

from security.password_validation import PasswordStrengthValidator
from security.upload_handlers import (
    ContentTypeValidationHandler,
    SecureFileUploadHandler
)


class SecurityHeadersTest(TestCase):
    """Test security headers are properly set."""
    
    def setUp(self):
        self.client = Client()
    
    def test_security_headers(self):
        """Test that all security headers are present."""
        response = self.client.get('/')
        
        # Check security headers
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['X-XSS-Protection'], '1; mode=block')
        self.assertTrue('Content-Security-Policy' in response)
        self.assertTrue('Strict-Transport-Security' in response)


class PasswordValidationTest(TestCase):
    """Test password validation rules."""
    
    def setUp(self):
        self.validator = PasswordStrengthValidator()
        self.User = get_user_model()
    
    def test_weak_passwords(self):
        """Test that weak passwords are rejected."""
        weak_passwords = [
            'password123',  # Too common
            'abc123',      # Too short
            '12345678',    # No special chars
            'abcdefgh',    # No numbers
            'ABCDEFGH',    # No lowercase
            'abcdefgh1',   # No uppercase
        ]
        
        for password in weak_passwords:
            with self.assertRaises(ValidationError):
                self.validator.validate(password)
    
    def test_strong_passwords(self):
        """Test that strong passwords are accepted."""
        strong_passwords = [
            'P@ssw0rd123!@#',
            'Str0ng_P@ssword',
            'C0mpl3x!P@ssw0rd',
        ]
        
        for password in strong_passwords:
            try:
                self.validator.validate(password)
            except ValidationError:
                self.fail(f"Password {password} should be valid")


class FileUploadTest(TestCase):
    """Test file upload security."""
    
    def setUp(self):
        self.handler = SecureFileUploadHandler()
        self.valid_image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        self.invalid_file = SimpleUploadedFile(
            "test.php",
            b"<?php echo 'hack'; ?>",
            content_type="application/x-php"
        )
    
    def test_valid_file_upload(self):
        """Test that valid files are accepted."""
        try:
            self.handler.handle_uploaded_file(self.valid_image)
        except ValidationError:
            self.fail("Valid image file should be accepted")
    
    def test_invalid_file_upload(self):
        """Test that invalid files are rejected."""
        with self.assertRaises(ValidationError):
            self.handler.handle_uploaded_file(self.invalid_file)
    
    def test_file_size_limit(self):
        """Test that large files are rejected."""
        large_file = SimpleUploadedFile(
            "large.jpg",
            b"x" * (6 * 1024 * 1024),  # 6MB
            content_type="image/jpeg"
        )
        with self.assertRaises(ValidationError):
            self.handler.handle_uploaded_file(large_file)


class CSRFProtectionTest(TestCase):
    """Test CSRF protection."""
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Str0ng_P@ssw0rd'
        )
    
    def test_csrf_required(self):
        """Test that CSRF token is required for POST requests."""
        self.client.login(username='testuser', password='Str0ng_P@ssw0rd')
        response = self.client.post('/api/some-endpoint/', {})
        self.assertEqual(response.status_code, 403)  # CSRF verification failed
    
    def test_csrf_token_accepted(self):
        """Test that requests with valid CSRF token are accepted."""
        self.client.login(username='testuser', password='Str0ng_P@ssw0rd')
        # Get CSRF token
        response = self.client.get('/api/some-endpoint/')
        csrf_token = response.cookies['csrftoken'].value
        
        # Make POST request with CSRF token
        response = self.client.post(
            '/api/some-endpoint/',
            {},
            HTTP_X_CSRFTOKEN=csrf_token
        )
        self.assertNotEqual(response.status_code, 403)  # Not CSRF error


class RateLimitTest(TestCase):
    """Test rate limiting."""
    
    def setUp(self):
        self.client = Client()
    
    def test_rate_limit(self):
        """Test that rate limiting is enforced."""
        # Make multiple requests quickly
        for _ in range(10):
            response = self.client.post('/api/login/', {
                'username': 'test',
                'password': 'test'
            })
        
        # Next request should be rate limited
        response = self.client.post('/api/login/', {
            'username': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 429)  # Too many requests


class SessionSecurityTest(TestCase):
    """Test session security settings."""
    
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Str0ng_P@ssw0rd'
        )
    
    def test_session_cookie_settings(self):
        """Test session cookie security settings."""
        self.client.login(username='testuser', password='Str0ng_P@ssw0rd')
        response = self.client.get('/')
        
        # Check session cookie settings
        session_cookie = response.cookies.get('sessionid')
        self.assertTrue(session_cookie['secure'])
        self.assertTrue(session_cookie['httponly'])
        self.assertEqual(session_cookie['samesite'], 'Strict')


class ContentSecurityPolicyTest(TestCase):
    """Test Content Security Policy."""
    
    def setUp(self):
        self.client = Client()
    
    def test_csp_headers(self):
        """Test that CSP headers are properly set."""
        response = self.client.get('/')
        csp = response['Content-Security-Policy']
        
        # Check CSP directives
        self.assertIn("default-src 'self'", csp)
        self.assertIn("script-src", csp)
        self.assertIn("style-src", csp)
        self.assertIn("img-src", csp)
        self.assertIn("connect-src", csp)
        self.assertIn("frame-ancestors", csp)
