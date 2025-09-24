from typing import Any, override

from django.db.models import QuerySet
from rest_framework import serializers, viewsets

from server.apps.payments.models import Payment
from server.apps.payments.serializers import PaymentSerializer
from server.di import resolve


class PaymentViewSet(viewsets.ModelViewSet[Payment]):

    serializer_class = PaymentSerializer
    http_method_names = ('get', 'create', 'patch')
