from rest_framework import serializers
from conversion.models import Conversion


class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = [
            'conversion_data',
            'created'
        ]
