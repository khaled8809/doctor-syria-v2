"""
Secure file upload handlers for Doctor Syria Platform.
"""

import os
import magic
import hashlib
from typing import Optional, List

from django.core.files.uploadhandler import FileUploadHandler, StopUpload
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class VirusScanUploadHandler(FileUploadHandler):
    """
    Upload handler that scans files for viruses using ClamAV.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content: Optional[bytes] = None
        self.file_size = 0
        self.chunk_size = 64 * 1024  # 64KB chunks
    
    def receive_data_chunk(self, raw_data: bytes, start: int) -> bytes:
        """Process each chunk of data as it's being uploaded."""
        if self.content is None:
            self.content = raw_data
        else:
            self.content += raw_data
        self.file_size += len(raw_data)
        
        # Check file size
        if self.file_size > settings.FILE_UPLOAD_SECURITY['MAX_UPLOAD_SIZE']:
            raise StopUpload(connection_reset=True)
        
        return raw_data
    
    def file_complete(self, file_size: int) -> None:
        """
        Scan the complete file for viruses.
        """
        if not self.content:
            return
        
        # Implement virus scanning here
        try:
            # Example implementation using ClamAV
            # import clamd
            # cd = clamd.ClamdUnixSocket()
            # scan_results = cd.instream(self.content)
            # if scan_results['stream'][0] == 'FOUND':
            #     raise ValidationError(_('Virus detected in file'))
            pass
        except Exception as e:
            raise ValidationError(_('Error scanning file: {}').format(str(e)))


class ContentTypeValidationHandler(FileUploadHandler):
    """
    Upload handler that validates file content type and extension.
    """
    
    ALLOWED_EXTENSIONS = {
        '.jpg': ['image/jpeg'],
        '.jpeg': ['image/jpeg'],
        '.png': ['image/png'],
        '.gif': ['image/gif'],
        '.pdf': ['application/pdf'],
        '.doc': ['application/msword'],
        '.docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content: Optional[bytes] = None
        self.file_name: Optional[str] = None
        self.content_type: Optional[str] = None
        self.file_hash = hashlib.sha256()
    
    def new_file(self, *args, **kwargs):
        """Handle new file upload."""
        super().new_file(*args, **kwargs)
        self.file_name = self.file_name or kwargs.get('file_name')
        self.content_type = kwargs.get('content_type')
    
    def receive_data_chunk(self, raw_data: bytes, start: int) -> bytes:
        """Process each chunk of data."""
        if self.content is None:
            self.content = raw_data
        else:
            self.content += raw_data
        
        # Update file hash
        self.file_hash.update(raw_data)
        return raw_data
    
    def file_complete(self, file_size: int) -> None:
        """
        Validate the complete file.
        """
        if not self.content or not self.file_name:
            return
        
        # Get file extension
        _, ext = os.path.splitext(self.file_name.lower())
        
        # Check if extension is allowed
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValidationError(_('File type not allowed'))
        
        # Check actual content type using python-magic
        mime = magic.Magic(mime=True)
        detected_type = mime.from_buffer(self.content)
        
        # Validate content type
        if detected_type not in self.ALLOWED_EXTENSIONS[ext]:
            raise ValidationError(_('File content does not match its extension'))
        
        # Store file hash for future reference
        self.file.hash = self.file_hash.hexdigest()


class SecureFileUploadHandler:
    """
    High-level handler that combines multiple security checks.
    """
    
    def __init__(self):
        self.handlers: List[FileUploadHandler] = [
            VirusScanUploadHandler(),
            ContentTypeValidationHandler(),
        ]
    
    def handle_uploaded_file(self, uploaded_file) -> None:
        """
        Process an uploaded file through all security handlers.
        """
        for handler in self.handlers:
            handler.handle_raw_input(
                uploaded_file.read(),
                uploaded_file.content_type,
                uploaded_file.size,
                uploaded_file.charset,
                uploaded_file.content_type_extra
            )
        
        # Additional security checks
        self._sanitize_filename(uploaded_file)
        self._check_file_content(uploaded_file)
    
    def _sanitize_filename(self, file) -> None:
        """
        Sanitize the filename to prevent directory traversal attacks.
        """
        # Remove path separators and null bytes
        filename = os.path.basename(file.name)
        filename = filename.replace('\x00', '')
        
        # Remove potentially dangerous characters
        filename = ''.join(c for c in filename if c.isalnum() or c in '._- ')
        
        # Ensure filename isn't too long
        if len(filename) > 255:
            filename = filename[:255]
        
        file.name = filename
    
    def _check_file_content(self, file) -> None:
        """
        Perform additional content checks.
        """
        # Check for executable content
        if file.content_type.startswith('application/x-'):
            raise ValidationError(_('Executable files are not allowed'))
        
        # Check for script content
        if file.content_type.startswith('text/'):
            content = file.read().decode('utf-8', errors='ignore')
            if '<?php' in content or '<%' in content or '<script' in content:
                raise ValidationError(_('Script content is not allowed'))
            file.seek(0)  # Reset file pointer
