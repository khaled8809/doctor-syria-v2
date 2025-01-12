"""
Password validation for Doctor Syria Platform.
"""

import re
from typing import Optional, List

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import get_default_password_validators


class PasswordStrengthValidator:
    """
    Validate that the password meets minimum security requirements.
    """
    
    def __init__(self, min_length=12, special_chars=True, numbers=True,
                 upper_case=True, lower_case=True):
        self.min_length = min_length
        self.special_chars = special_chars
        self.numbers = numbers
        self.upper_case = upper_case
        self.lower_case = lower_case
    
    def validate(self, password: str, user=None) -> None:
        """
        Validate whether the password meets all requirements.
        """
        if len(password) < self.min_length:
            raise ValidationError(
                _('Password must be at least %(min_length)d characters long.'),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        
        # Check for special characters
        if self.special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _('Password must contain at least one special character.'),
                code='password_no_special',
            )
        
        # Check for numbers
        if self.numbers and not re.search(r'\d', password):
            raise ValidationError(
                _('Password must contain at least one number.'),
                code='password_no_number',
            )
        
        # Check for uppercase letters
        if self.upper_case and not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('Password must contain at least one uppercase letter.'),
                code='password_no_upper',
            )
        
        # Check for lowercase letters
        if self.lower_case and not re.search(r'[a-z]', password):
            raise ValidationError(
                _('Password must contain at least one lowercase letter.'),
                code='password_no_lower',
            )
        
        # Check for common patterns
        self._check_common_patterns(password)
        
        # Check for keyboard patterns
        self._check_keyboard_patterns(password)
    
    def _check_common_patterns(self, password: str) -> None:
        """
        Check for common password patterns.
        """
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            raise ValidationError(
                _('Password contains too many repeated characters.'),
                code='password_repeated_chars',
            )
        
        # Check for sequential numbers
        if any(str(i) in password for i in range(1000)):
            raise ValidationError(
                _('Password contains sequential numbers.'),
                code='password_sequential_numbers',
            )
        
        # Check for sequential letters
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(len(alphabet) - 2):
            if alphabet[i:i + 3].lower() in password.lower():
                raise ValidationError(
                    _('Password contains sequential letters.'),
                    code='password_sequential_letters',
                )
    
    def _check_keyboard_patterns(self, password: str) -> None:
        """
        Check for keyboard patterns.
        """
        keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn', '123456', '098765',
            'qwertz', 'azerty',
        ]
        
        password_lower = password.lower()
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                raise ValidationError(
                    _('Password contains a keyboard pattern.'),
                    code='password_keyboard_pattern',
                )
    
    def get_help_text(self) -> str:
        """
        Return help text for this validator.
        """
        help_texts = [
            _('Your password must contain at least %(min_length)d characters.') % {
                'min_length': self.min_length}
        ]
        
        if self.special_chars:
            help_texts.append(_('Your password must contain at least one special character.'))
        if self.numbers:
            help_texts.append(_('Your password must contain at least one number.'))
        if self.upper_case:
            help_texts.append(_('Your password must contain at least one uppercase letter.'))
        if self.lower_case:
            help_texts.append(_('Your password must contain at least one lowercase letter.'))
        
        return ' '.join(help_texts)


def validate_password(password: str, user=None) -> List[ValidationError]:
    """
    Validate a password against all validators.
    """
    errors = []
    validators = get_default_password_validators()
    
    for validator in validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.extend(error.error_list)
    
    if errors:
        raise ValidationError(errors)
    
    return errors


def get_password_strength(password: str) -> dict:
    """
    Calculate password strength score and provide feedback.
    """
    score = 0
    feedback = []
    
    # Length score (up to 30 points)
    length_score = min(len(password) * 2, 30)
    score += length_score
    
    # Character variety score (up to 40 points)
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'\d', password):
        score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 10
    
    # Complexity score (up to 30 points)
    if len(set(password)) > 8:  # Unique characters
        score += 10
    if not re.search(r'(.)\1{2,}', password):  # No repeated chars
        score += 10
    if len(password) > 14:  # Extra length bonus
        score += 10
    
    # Generate feedback
    if score < 50:
        feedback.append(_('This is a weak password. Please make it stronger.'))
    elif score < 70:
        feedback.append(_('This is a moderate password. Consider making it stronger.'))
    else:
        feedback.append(_('This is a strong password.'))
    
    if len(password) < 12:
        feedback.append(_('Consider using a longer password.'))
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        feedback.append(_('Add special characters to make the password stronger.'))
    if not re.search(r'\d', password):
        feedback.append(_('Add numbers to make the password stronger.'))
    
    return {
        'score': score,
        'strength': 'weak' if score < 50 else 'moderate' if score < 70 else 'strong',
        'feedback': feedback,
    }
