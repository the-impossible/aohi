from django.core.exceptions import ValidationError

def validate_pic_size(value):
    picsize = value.size

    if picsize > 2097152:
        raise ValidationError('The maximum file size that can be uploaded is 2MB')