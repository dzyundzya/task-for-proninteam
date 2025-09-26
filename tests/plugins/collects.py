from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, TypedDict, Unpack

import pytest
from django.utils import timezone

from server.apps.collects.choices import OccasionType
from server.apps.collects.models import Collect
from server.apps.users.models import CustomUser

if TYPE_CHECKING:
    from tests.plugins.fakery import FakeryM

type CollectFactory = Callable[[Unpack[_CollectFactoryParams]], Collect]

type CollectBatchFactory = Callable[[int], list[Collect]]


class _CollectFactoryParams(TypedDict, total=False):
    """Base params for CollectFactory."""

    author: CustomUser
    title: str
    occasion: OccasionType
    description: str
    planned_amount: Decimal
    end_date: datetime


@pytest.fixture
def collect_factory(fakery_m: FakeryM[Collect]) -> CollectFactory:
    """Return a factory to create Collect instances with custom fields."""

    def factory(**kwargs: Unpack[_CollectFactoryParams]) -> Collect:
        return fakery_m(Collect)(**kwargs)

    return factory


@pytest.fixture
def collect(collect_factory: CollectFactory, auth_user: CustomUser) -> Collect:
    """Return a single Collect instance created."""
    return collect_factory(
        author=auth_user,
        title='Test title',
        description='Test description',
        planned_amount=Decimal(5000),
        end_date=timezone.now() + timedelta(days=25),
    )


@pytest.fixture
def collect_batch(collect_factory: CollectFactory) -> CollectBatchFactory:
    """Return a factory that creates `batch_size` Collect instances."""

    def factory(batch_size: int) -> list[Collect]:
        return [
            collect_factory(
                title=f'Tets title{collect_number}',
                description=f'Tets description{collect_number}',
            )
            for collect_number in range(batch_size)
        ]

    return factory
