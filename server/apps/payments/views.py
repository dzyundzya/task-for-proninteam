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
    http_method_names = ('get', 'post', 'patch')

    def get_queryset(self) -> QuerySet[Payment]:
        """Get queryset filtered by current user."""
        queryset = self.repo.get_all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def partial_update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Partial update paument using repo."""
        payment = self.repo.get_by_pk(kwargs['pk'])
        serlializer = self.get_serializer(
            payment, data=request.data, partial=True
        )
        serlializer.is_valid(raise_exception=True)
        upd_payment = self.repo.update_payment(payment, **serlializer.validated_data)
        return Response(
            self.get_serializer(upd_payment).data,
            status=status.HTTP_202_ACCEPTED
        )
    
    @property
    def repo(self) -> PaymentRepo:
        """Get DepartmentRepo instance from dependency container."""
        return resolve(PaymentRepo)

