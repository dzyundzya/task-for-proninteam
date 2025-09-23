from django.db import models


class OccasionType(models.TextChoices):
    """Choices for type of occasion."""

    BIRTHDAY = 'birthday', 'Birthday'
    WEDDING = 'wedding', 'Wedding'
    CHARITY = 'charity', 'Charity'
    MEDICAL = 'medical', 'Medical'
    EDUCATION = 'education', 'Education'
    TRAVEL = 'travel', 'Travel'
    BUSINESS = 'business', 'Business'
    OTHER = 'other', 'Other'
