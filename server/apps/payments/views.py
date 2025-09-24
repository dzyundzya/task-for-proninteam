from typing import Any, override

from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.payments.infra.repository import PaymentRepo
from server.apps.payments.models import Payment
from server.apps.payments.serializers import PaymentSerializer
from server.di import resolve


class PaymentViewSet(viewsets.ModelViewSet[Payment]):

    serializer_class = PaymentSerializer
    http_method_names = ('get', 'create', 'patch')

    def get_queryset(self) -> QuerySet[Payment]:
        """Get queryset using repo."""
        repo = resolve(PaymentRepo)
        return repo.get_all()
    
    def partial_update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Partial update paument using repo."""
        repo = resolve(PaymentRepo)
        payment = repo.get_by_pk(kwargs['pk'])
        serlializer = self.get_serializer(
            payment, data=request.data, partial=True
        )
        serlializer.is_valid(raise_exception=True)
        upd_payment = repo.update_payment(payment, **serlializer.validated_data)
        return Response(
            self.get_serializer(upd_payment).data,
            status=status.HTTP_202_ACCEPTED
        )
