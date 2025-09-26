from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from typing import TYPE_CHECKING, TypedDict, Unpack

import pytest
from django.utils import timezone

from server.apps.collects.models import Collect
from server.apps.payments.models import Payment
from server.apps.users.models import CustomUser

if TYPE_CHECKING:
    from tests.plugins.fakery import FakeryM  

type PaymentFactory = Callable[
    [Unpack[_PaymentFactoryParams]], Payment
]

type PaymentBatchFactory = Callable[[int], list[Payment]]


class _PaymentFactoryParams(TypedDict, total=False):
    """Base params for PaymentFactory."""

    user: CustomUser
    collect: Collect
    amount: Decimal
    comment: str
    paid: bool
    payment_day: timezone.datetime


@pytest.fixture
def payment_factory(fakery_m: FakeryM[Payment]) -> PaymentFactory:
    """Return a factory to create Payment instances with custom fields."""

    def factory(**kwargs: Unpack[_PaymentFactoryParams]) -> Payment:
        return fakery_m(Payment)(**kwargs)

    return factory


@pytest.fixture
def payment(payment_factory: PaymentFactory) -> Payment:
    """Return a single Payment instance created."""
    return payment_factory(
        amount=Decimal(100),
        comment='Test_comment',
        paid=True,
        payment_day=timezone.now()
    )


@pytest.fixture
def payment_batch(payment_factory: PaymentFactory) -> PaymentBatchFactory:
    """Return a factory that creates `batch_size` Payment instances."""

    def factory(batch_size: int) -> list[Payment]:
        return [
            payment_factory(comment=f'Test_comment{payment_number}')
            for payment_number in range(batch_size)
        ]

    return factory
