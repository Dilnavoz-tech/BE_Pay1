
import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from cards.utils import generate_otp_code


def validate_pan(value):
    if len(str(value)) != 16:
        raise ValidationError('Pan must be 16 digits')

def validate_expire_month(value):
    if not (1 <= value <= 12):
        raise ValidationError('Invalid expire month')

def validate_expire_year(value):
    current_year = timezone.now().year
    if not value > current_year:
        raise ValidationError('Invalid expire year')

def validate_uz_phone_number(phone_number: str):
    phone_number = phone_number.replace(' ', '')
    if len(phone_number) != 12:
        raise ValidationError("Length should be 12")
    if not phone_number.startswith('998'):
        raise ValidationError("Phone number should start with 998")
    if not phone_number[1:].isdigit():
        raise ValidationError("Phone number should consist of digits (0-9)")

class BaseCard(models.Model):
    pan = models.IntegerField(default=0, validators=[validate_pan])
    expire_month = models.IntegerField(default=0, validators=[validate_expire_month])
    expire_year = models.IntegerField(default=0, validators=[validate_expire_year])

    holder_full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=12, validators=[validate_uz_phone_number])

    balance = models.IntegerField(default=0)

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.holder_full_name

    class Meta:
        abstract = True


class HumoCard(BaseCard):
    pass

class UzCard(BaseCard):
    pass

class VisaCard(BaseCard):
    pass

class MasterCard(BaseCard):
    pass


class OTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=generate_otp_code)
    phone_number = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
