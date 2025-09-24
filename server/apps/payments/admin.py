from django.contrib import admin

from server.apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'collect', 'amount', 'paid', 'created_at')
    search_fields = (
        'collect__title',
        'user__username',
        'user__email',
    )
    list_filter = ('paid', 'created_at',)
    
    list_select_related = ('user', 'collect')
    list_per_page = 25
    ordering = ('-created_at',)
