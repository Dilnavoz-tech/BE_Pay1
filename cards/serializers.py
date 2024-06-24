from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer
from .models import HumoCard, UzCard, validate_pan, validate_expire_year, validate_expire_month
from .validators import validate_uzcard_data


class HumoCardSerializer(ModelSerializer):
    class Meta:
        model = HumoCard
        fields = 'pan', 'holder_full_name', 'phone_number', 'expire_month', 'expire_year'
        read_only_fields = ('created_at', 'updated_at')

class CardSerializer(ModelSerializer):
    class Meta:
        model = HumoCard
        fields = '__all_'

class UzCardSerializer(ModelSerializer):
    pan = CharField(validators=[validate_pan])
    expire_year = IntegerField(validators=[validate_expire_year])
    expire_month = IntegerField(validators=[validate_expire_month])

    class Meta:
        model = UzCard
        fields = ['holder_full_name', 'phone_number', 'pan', 'expire_year', 'expire_month',  'balance']

    def validate(self, data):
        return validate_uzcard_data(data)

class CarduzSerializer(ModelSerializer):
    class Meta:
        model = HumoCard
        fields = 'pan', 'holder_full_name', 'phone_number', 'expire_month', 'expire_year'
        read_only_fields = ('created_at', 'updated_at')


