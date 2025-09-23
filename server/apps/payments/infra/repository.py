from typing import final

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
        return Payment.objects.select_related('user', 'collect').get(pk=pk)
