from typing import Any

from django.utils.timezone import now
from rest_framework import serializers

from server.apps.collects.models import Collect
from server.apps.collects.services import CollectAmountService
from server.apps.users.serializers import UserSerializer


class CollectSerializer(serializers.ModelSerializer[Collect]):  # type: ignore[misc]
    """Serializer for Collect model."""

    is_unlimited = serializers.ReadOnlyField()
    progress_percentage = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'occasion',
            'description',
            'planned_amount',
            'current_amount',
            'donations_count',
            'cover_image',
            'end_date',
            'is_active',
            'is_unlimited',
            'progress_percentage',
            'days_remaining',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'current_amount',
            'donations_count',
            'is_unlimited',
            'progress_percentage',
            'days_remaining',
            'created_at',
            'updated_at',
        )

    def validate(self, collect_data: dict[str, Any]) -> dict[str, Any]:
        """Validate collect data."""
        end_date = collect_data.get('end_date')
        if end_date and end_date <= now():
            raise serializers.ValidationError({
                'end_date': 'The end date should be in the future.'
            })

        planned_amount = collect_data.get('planned_amount')
        if planned_amount and planned_amount < 0:
            raise serializers.ValidationError({
                'planned_amount': 'The target amount cannot be negative.'
            })
        return collect_data

    def create(self, validated_data: dict[str, Any]) -> Any:
        """Create a new collect instance."""
        validated_data['author'] = self.context['request'].user
        collect = super().create(validated_data)

        CollectAmountService.update_collect_amounts(collect)
        return collect
