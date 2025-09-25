from django.contrib import admin

from server.apps.collects.models import Collect


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin[Collect]):
    """Admin interface for the Collect model."""
    list_display = (
        'id',
        'title',
        'author',
        'occasion',
        'current_amount',
        'end_date',
        'is_active',
        'created_at',
    )
    search_fields = (
        'title',
        'author__username',
        'author__email',
        'description',
    )
    list_filter = ('occasion', 'is_active', 'end_date')
    list_select_related = ('author',)
    list_per_page = 50
    ordering = ('-created_at',)
    readonly_fields = (
        'current_amount',
        'donations_count',
        'created_at',
        'updated_at',
    )
