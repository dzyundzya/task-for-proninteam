from unittest.mock import Mock

import pytest

from server.apps.payments.models import Payment
from server.apps.payments.serializers import PaymentSerializer


@pytest.mark.django_db
def test_update_payment_same_paid_status_no_recalculation(
    payment: Payment, mocker: Mock
) -> None:
    """Test that same paid status doesn't trigger recalculation."""
    mock_update = mocker.patch(
        'server.apps.collects.services.CollectAmountService.update_collect_amounts'
    )

    serializer = PaymentSerializer()
    validated_data = {'comment': 'Updated comment'}

    updated_payment = serializer.update(payment, validated_data)

    mock_update.assert_not_called()
    assert updated_payment.comment == 'Updated comment'


@pytest.mark.django_db
def test_update_payment_changes_paid_status_triggers_recalculation(
    payment: Payment, mocker: Mock
) -> None:
    """Test that changing paid status triggers recalculation."""
    mock_update = mocker.patch(
        'server.apps.collects.services.CollectAmountService.update_collect_amounts'
    )
    serializer = PaymentSerializer()
    new_paid_status = not payment.paid
    validated_data = {'comment': 'Updated comment', 'paid': new_paid_status}

    updated_payment = serializer.update(payment, validated_data)

    mock_update.assert_called_once_with(payment.collect)
    assert updated_payment.comment == 'Updated comment'
    assert updated_payment.paid == new_paid_status


@pytest.mark.django_db
def test_update_payment_no_paid_field_in_validated_data(
    payment: Payment, mocker: Mock
) -> None:
    """Test that no paid field doesn't trigger recalculation."""
    mock_update = mocker.patch(
        'server.apps.collects.services.CollectAmountService.update_collect_amounts'
    )
    serializer = PaymentSerializer()
    validated_data = {'comment': 'Updated comment'}
    updated_payment = serializer.update(payment, validated_data)
    mock_update.assert_not_called()

    assert updated_payment.comment == 'Updated comment'
    assert updated_payment.paid == payment.paid
