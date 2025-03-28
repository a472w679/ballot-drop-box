# api/serializers.py
from rest_framework import serializers

from .models import EnvelopeScan


class EnvelopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvelopeScan
        fields = '__all__'
        extra_kwargs = {
            'imb': {'required': False, 'allow_blank': True, 'allow_null': True},
            'streetaddress': {'required': False, 'allow_blank': True, 'allow_null': True},
            'city': {'required': False, 'allow_blank': True, 'allow_null': True},
            'zipcode': {'required': False, 'allow_blank': True, 'allow_null': True},
            'status': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

