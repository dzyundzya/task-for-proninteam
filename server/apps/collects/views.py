from typing import Any

from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.collects.infra.repository import CollectRepo
from server.apps.collects.models import Collect
from server.apps.collects.serializers import CollectSerializer
from server.di import resolve


class CollectViewSet(viewsets.ModelViewSet[Collect]):  # type: ignore[misc]  # noqa: WPS214
    """ViewSet for managing collects."""

    serializer_class = CollectSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self) -> QuerySet[Collect]:
        """Get queryset using repo."""
        return {'list': self.repo.get_all_active()}.get(
            self.action, self.repo.get_all()
        )

    def get_serializer_context(self) -> Any:
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List all collects with pagination."""
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a specific collect by ID."""
        collect = self.repo.get_by_pk(kwargs['pk'])
        serializer = self.get_serializer(collect)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new collect."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collect = serializer.save()
        return Response(
            self.get_serializer(collect).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Partially update a collect (only by author)."""
        collect = self.repo.get_by_pk(kwargs['pk'])
        if collect.author != request.user:
            return Response(
                {'error': 'You can edit only your own collections.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(
            collect, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        upd_collect = serializer.save()
        return Response(
            self.get_serializer(upd_collect).data,
            status=status.HTTP_202_ACCEPTED,
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Soft delete a collect (only by author)."""
        collect = self.repo.get_by_pk(kwargs['pk'])
        if collect.author != request.user:
            return Response(
                {'error': 'You can delete only your own collections.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        collect.is_active = False
        collect.save(update_fields=('is_active', 'updated_at'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @property
    def repo(self) -> CollectRepo:
        """Return an instance of CollectRepo."""
        return resolve(CollectRepo)
