from typing import Any, final

from django.db.models import QuerySet

from server.apps.payments.models import Payment


@final
class PaymentRepo:
    """Repository for Collect model."""

    def get_all(self) -> QuerySet[Payment]:
        """Returns all collect options from DB."""
        return Payment.objects.select_related('user', 'collect').all()

    def get_by_pk(self, pk: int) -> Payment:
        """Returns one collect option from DB by pk."""
        return self.get_all().get(pk=pk)

    def update_payment(self, payment: Payment, **kwargs: Any) -> Payment:
        """Update an existing payment."""
        Payment.objects.filter(pk=payment.pk).update(**kwargs)
        payment.refresh_from_db()
        return payment
