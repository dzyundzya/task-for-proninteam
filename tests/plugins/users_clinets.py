from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, TypedDict, Unpack

import pytest
from rest_framework.test import APIClient

from server.apps.users.models import CustomUser

if TYPE_CHECKING:
    from tests.plugins.fakery import FakeryM

type UserFactory = Callable[[Unpack[_UserFactoryParams]], CustomUser]

type UserBatchFactory = Callable[[int], list[CustomUser]]


class _UserFactoryParams(TypedDict, total=False):
    """Base params for UserFactory."""

    username: str
    email: str
    first_name : str
    last_name: str
    password: str
    is_active: bool


@pytest.fixture
def user_factory(fakery_m: FakeryM[CustomUser]) -> UserFactory:
    """Factory fixture for creating User instances."""

    def factory(**kwargs: Unpack[_UserFactoryParams]) -> CustomUser:
        return fakery_m(CustomUser)(**kwargs)

    return factory


@pytest.fixture
def auth_user(user_factory: UserFactory) -> CustomUser:
    """Fixture that create a single User instance."""
    return user_factory(
        username='testuser',
        email='test@example.com',
        first_name='first_name_test',
        last_name='last_name_test',
        is_active=True,
    )


@pytest.fixture
def auth_none_author(user_factory: UserFactory) -> CustomUser:
    """Fixture that create a single nene author User instance."""
    return user_factory(
        username='testnoneuser',
        email='tesnonet@example.com',
        first_name='first_name_test',
        last_name='last_name_test',
        is_active=True,
    )


@pytest.fixture
def api_client() -> APIClient:
    """API client."""
    return APIClient()


@pytest.fixture
def auth_client(api_client: APIClient, auth_user: CustomUser) -> APIClient:
    """Return an authenticated APIClient for testing."""
    api_client.force_authenticate(user=auth_user)
    return api_client


@pytest.fixture
def auth_none_author_client(
    api_client: APIClient, auth_none_author: CustomUser
    ) -> APIClient:
    """Return an authenticated APIClient for testing."""
    api_client.force_authenticate(user=auth_none_author)
    return api_client