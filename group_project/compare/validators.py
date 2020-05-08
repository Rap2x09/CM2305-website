import os
from django.core.exceptions import ValidationError

def validate_file(value):
    get_ext = os.path.splitext(value.name)[1]
    extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not get_ext.lower() in extensions:
        raise ValidationError('Invalid file extension.')