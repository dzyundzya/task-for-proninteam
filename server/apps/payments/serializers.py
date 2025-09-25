from typing import Any

from rest_framework import serializers

from server.apps.collects.services import CollectAmountService
from server.apps.payments.models import Payment
from server.apps.users.serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer[Payment]):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'collect',
            'amount',
            'comment',
            'paid',
            'payment_day',
            'created_at',
        )

    def create(self, validated_data: dict[str, Any]) -> Any:
        validated_data['user'] = self.context['request'].user
        payment = super().create(validated_data)
        CollectAmountService.update_collect_amounts(payment.collect)
        return payment

    def update(self, instance: Payment, validated_data: dict[str, Any]) -> Any:
        old_paid_status = instance.paid
        new_paid_status = validated_data.get('paid', old_paid_status)
        payment = super().update(instance, validated_data)

        if new_paid_status != old_paid_status:
            CollectAmountService.update_collect_amounts(payment.collect)
        return payment
