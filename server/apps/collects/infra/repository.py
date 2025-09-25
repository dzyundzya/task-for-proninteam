from typing import final

from django.db.models import QuerySet

from server.apps.collects.models import Collect


@final
class CollectRepo:
    """Repository for Collect model."""

    def get_all(self) -> QuerySet[Collect]:
        """Returns all collect options from DB."""
        return Collect.objects.select_related('author').all()

    def get_all_active(self) -> QuerySet[Collect]:
        """Returns all is_active collect options from DB."""
        return Collect.objects.select_related('author').filter(is_active=True)

    def get_by_pk(self, pk: int) -> Collect:
        """Returns one collect option from DB by pk."""
        return Collect.objects.select_related('author').get(pk=pk)
