from typing import override

from django.core.validators import MinValueValidator
from django.db import models

from server.common import constants



class Payment(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='User',
    )
    collect = models.ForeignKey(
        'collects.Collect',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Collect',
    )
    amount = models.DecimalField(
        'Amount',
        max_digits=constants.MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        validators=[
            MinValueValidator(constants.ONE),
        ],
    )
    comment = models.TextField('Comment', blank=True)
    paid = models.BooleanField('Paid', default=False)
    payment_day = models.DateTimeField('Payment day', blank=True, null=True)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'Payments'
        ordering = ('-created_at',)

    @override
    def __str__(self) -> str:
        return f'{self.user.username}: {self.amount} rub.'
    
    @override
    def save(self, *args, **kwargs) -> None:
        from server.apps.payments.infra.repository import PaymentRepo
        from server.di import resolve
        is_new = self._state.adding
        old_paid = None
        repo = resolve(PaymentRepo)

        if not is_new:
            try:
                old_paid = repo.get_by_pk(pk=self.pk).paid
            except Payment.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if is_new and self.paid or (not is_new and self.paid != old_paid):
            self.collect.update_amounts()
