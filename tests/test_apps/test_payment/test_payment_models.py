import pytest

from server.apps.payments.models import Payment


@pytest.mark.django_db
def test_str_method_payment(payment: Payment) -> None:
    """Test string representation of Payment."""
    expected_str = f'{payment.user.username}: {payment.amount} rub.'
    assert str(payment) == expected_str
