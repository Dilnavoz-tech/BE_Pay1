from django.core.exceptions import ValidationError

def validate_uzcard_data(data):
    required_fields = ['holder_full_name', 'phone_number',  'pan', 'expire_year', 'expire_month', 'balance']
    for field in required_fields:
        if field not in data:
            raise ValidationError({field: f"{field} is required."})
    return data
