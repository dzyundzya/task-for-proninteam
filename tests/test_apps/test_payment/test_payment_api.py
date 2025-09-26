from decimal import Decimal
from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APIClient

from server.apps.collects.models import Collect
from server.apps.payments.models import Payment
from server.apps.payments.views import PaymentViewSet


@pytest.mark.django_db
def test_create_payment(auth_client: APIClient, collect: Collect) -> None:
    """Successfully creating a payment returns 201 and correct JSON."""
    url = reverse('payments-list')
    payload = {
        'collect': collect.id,
        'amount': Decimal(500),
        'comment': 'Test comment',
        'paid': True,
        'payment_day': now(),
    }

    response = auth_client.post(url, payload, format='json')
    response_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_data['comment'] == 'Test comment'
    assert 'id' in response_data

    payment = Payment.objects.get(id=response_data['id'])
    assert payment.comment == 'Test comment'


@pytest.mark.django_db
def test_patch_success(
    collect: Collect, payment: Payment, auth_client: APIClient
) -> None:
    """Successfully partial updating a payment."""
    url = reverse('payments-detail', kwargs={'pk': payment.pk})
    payload = {
        'amount': Decimal(1000),
        'comment': 'Upd comment',
        'paid': True,
    }
    response = auth_client.patch(url, payload, format='json')
    response_data = response.json()

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response_data['comment'] == payload['comment']


@pytest.mark.django_db
def test_get_queryset(payment: Payment, auth_client: APIClient) -> None:
    """Test that get_queryset returns payments with proper filtering."""
    viewset = PaymentViewSet()
    queryset = viewset.get_queryset()
    assert queryset.count() == 1


@pytest.mark.django_db
def test_patch_by_none_author(
    payment: Payment, auth_none_author_client: APIClient
) -> None:
    """Test that non-owner cannot patch a payment."""
    url = reverse('payments-detail', kwargs={'pk': payment.pk})
    payload = {
        'comment': 'Update_comment',
    }
    response = auth_none_author_client.patch(url, payload, format='json')

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_by_none_author(
    payment: Payment, auth_none_author_client: APIClient
) -> None:
    """Test that non-author user can retrieve payment details and list."""
    url_detail = reverse('payments-detail', kwargs={'pk': payment.pk})
    response_detail = auth_none_author_client.get(url_detail)

    assert response_detail.status_code == HTTPStatus.OK

    url = reverse('payments-list')
    response = auth_none_author_client.get(url)

    assert response.status_code == HTTPStatus.OK
