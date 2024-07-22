from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ModelSerializer

from users.models import Payment


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
