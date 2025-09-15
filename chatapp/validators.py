from django.core.exceptions import ValidationError

def validate_file_type(value):
    valid_types = ['image/*', 'video/*', 'application/pdf']
    if not value.file.content_type in valid_types:
        raise ValidationError('Unsupported file type')

def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10MB
    if value.size > limit:
        raise ValidationError('File too large')
