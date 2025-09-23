from typing import override

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

from server.apps.collects.choices import OccasionType
from server.common import constants

class  Collect(models.Model):
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='collects',
        verbose_name='Author'
    )
    title = models.CharField('Title', max_length=constants.TITLE_LENGTH)
    occasion = models.CharField(
        'Occasion',
        max_length=constants.OCCASION_LENGTH,
        choices=OccasionType.choices,
        default=OccasionType.OTHER,
    )
    description = models.TextField('Description', blank=True)
    planned_amount = models.DecimalField(
        'Amount planned',
        max_digits=constants.MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        null=True, blank=True,
        help_text=constants.PLANNED_HELP_TEXT,
        validators=[MinValueValidator(constants.ZERO),],
    )
    current_amount = models.DecimalField(
        'Amount current',
        max_digits=constants.MAX_DIGITS,
        decimal_places=constants.DECIMAL_PLACES,
        default=constants.ZERO,
        validators=[MinValueValidator(constants.ZERO),],
    )
    donations_count = models.PositiveIntegerField(
        'Number of donations',
        default=constants.ZERO,
    )
    cover_image = models.ImageField(
        'Cover',
        upload_to=constants.UPLOAD_TO,
        blank=True
    )
    end_date = models.DateTimeField('End date', null=True, blank=True)
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    class Meta:
        verbose_name = 'collect'
        verbose_name_plural = 'Collects'
        ordering = ('-created_at',)
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_collect_per_author',
            ),
        )

    @override
    def __str__(self) -> str:
        return self.title
    
    @property
    def is_unlimited(self) -> bool:
        """Checks whether the collection is infinite."""
        return self.planned_amount is None
    
    @property
    def progress_percentage(self) -> int:
        """Percentage of the collected amount."""
        if self.is_unlimited or self.planned_amount == 0:
            return 0
        return min(100, (self.current_amount / self.planned_amount) * 100)
    
    @property
    def days_remaining(self) -> None | int:
        """The remaining number of days until completion."""
        if not self.end_date:
            return None
        remaining = self.end_date - now()
        return max(0, remaining.days)


