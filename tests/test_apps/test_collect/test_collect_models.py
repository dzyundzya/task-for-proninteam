from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest
from django.utils.timezone import now

from server.apps.collects.models import Collect


@pytest.mark.django_db
def test_str_method_collect(collect: Collect) -> None:
    """Test string representation of Collect."""
    assert str(collect) == collect.title


@pytest.mark.django_db
def test_is_unlimited(collect: Collect) -> None:
    """Test is_unlimited returns True when planned_amount is None."""
    collect.planned_amount = None
    assert collect.is_unlimited is True
    assert collect.planned_amount is None


@pytest.mark.parametrize(
    'planned_amount, current_amount, exepted_result',
    [
        (Decimal(1000), Decimal(500), 50),
        (Decimal(1000), Decimal(750), 75),
        (None, Decimal(500), 0)
    ]
)
@pytest.mark.django_db
def test_progress_percentage(
    collect: Collect, 
    planned_amount: Decimal | None, 
    current_amount: Decimal,
    exepted_result: int
) -> None:
    collect.planned_amount=planned_amount
    collect.current_amount=current_amount
    assert collect.progress_percentage == exepted_result


@pytest.mark.parametrize(
    'end_date, exepted_result',
    [
        (None, (None,)),
        (now() + timedelta(days=10), (9,10))
    ]
)
@pytest.mark.django_db
def test_days_remaining(
    collect: Collect,
    end_date: datetime | None,
    exepted_result: tuple[Any]
) -> None:
    collect.end_date=end_date
    assert collect.days_remaining in exepted_result
    