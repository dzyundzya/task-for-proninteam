import pytest

from server.apps.payments.infra.repository import PaymentRepo
from server.apps.payments.models import Payment
from server.di import resolve
from tests.plugins.payments import PaymentBatchFactory


@pytest.mark.django_db
def test_get_all(payment_batch: PaymentBatchFactory) -> None:
    """Test the `get_all()` method of PaymentRepo."""
    batch_size = 2
    payment_batch(batch_size)

    repo = resolve(PaymentRepo)
    all_payments = repo.get_all()

    assert all_payments.count() == batch_size


@pytest.mark.django_db
def test_get_by_pk(payment: Payment) -> None:
    """Test the `get_by_pk()` method of PaymentRepo."""
    repo = resolve(PaymentRepo)
    payment_obj = repo.get_by_pk(pk=payment.id)

    assert payment_obj == payment


@pytest.mark.django_db
def test_get_by_pk_none() -> None:
    """get_by_pk raises Payment.DoesNotExist if object is missing."""
    repo = resolve(PaymentRepo)
    with pytest.raises(Payment.DoesNotExist):
        repo.get_by_pk(pk=1)


@pytest.mark.django_db
def test_partial_update_payment(payment: Payment) -> None:
    """Test PaymentRepo update_payment method."""
    repo = resolve(PaymentRepo)
    original_comment = payment.comment
    upd_payment_obj = repo.update_payment(
        payment=payment, comment='Update comment'
    )
    assert upd_payment_obj.comment == 'Update comment'
    assert upd_payment_obj.comment != original_comment
