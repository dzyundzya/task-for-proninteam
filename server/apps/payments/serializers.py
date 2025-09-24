from rest_framework import serializers

from server.apps.payments.models import Payment
from server.apps.users.serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 
            'user', 
            'amount', 
            'comment', 
            'paid', 
            'payment_day', 
            'created_at'
        )
