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
        validators=[MinValueValidator(constants.ONE),],
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
        return '{username}: {amount} rub.'.format(
        username=self.user.username,
        amount=self.amount,
    )
