from django.db.models import Sum, Count

from server.apps.collects.models import Collect
from server.apps.payments.models import Payment


class CollectAmountService:

    @staticmethod
    def update_collect_amounts(collect: Collect) -> None:
        aggregated_data = Payment.objects.filter(
            collect=collect,
            paid=True,
        ).aggregate(
            total_amount=Sum('amount'),
            unique_donors=Count('user', distinct=True)
        )

        collect.current_amount = aggregated_data['total_amount'] or 0
        collect.donations_count = aggregated_data['unique_donors'] or 0
        collect.save(update_fields=(
            'current_amount', 'donations_count', 'updated_at'
        ))

    @classmethod
    def recalculate_all_collects(cls) -> None:
        for collect in Collect.objects.all():
            cls.update_collect_amounts(collect)
