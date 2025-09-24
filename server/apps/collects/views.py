from typing import Any

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.collects.infra.repository import CollectRepo
from server.apps.collects.models import Collect
from server.apps.collects.serializers import CollectSerializer
from server.di import resolve


class CollectViewSet(viewsets.ModelViewSet[Collect]):
    serializer_class = CollectSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_context(self) -> Any:
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    