from datetime import timedelta
from decimal import Decimal
from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from server.apps.collects.models import Collect
from server.apps.collects.serializers import CollectSerializer
from tests.plugins.collects import CollectBatchFactory


@pytest.mark.django_db
def test_validate_past_end_date(auth_client: APIClient) -> None:
        """Test validate raises error for past end_date."""
        serializer = CollectSerializer(context={'request': None})
        
        invalid_data = {
            'title': 'Invalid Collect',
            'occasion': 'Birthday',
            'end_date': now() - timedelta(days=1),
            'planned_amount': Decimal('1000.00')
        }
        
        with pytest.raises(ValidationError) as exc_info:
            serializer.validate(invalid_data)


@pytest.mark.django_db
def test_validate_negative_planned_amount(auth_client: APIClient) -> None:
    """Test validation raises error for negative planned_amount."""
    serializer = CollectSerializer(context={'request': None})
    
    invalid_data = {
        'planned_amount': Decimal('-100.00')
    }
    
    with pytest.raises(ValidationError) as exc_info:
        serializer.validate(invalid_data)


@pytest.mark.django_db
def test_validate_positive(auth_client: APIClient) -> None:
    """Test validation allows positive planned_amount."""
    serializer = CollectSerializer(context={'request': None})
    
    valid_data = {
        'end_date': now() + timedelta(days=5),
        'planned_amount': Decimal('1000.00')
    }
    
    positive_result = serializer.validate(valid_data)
    assert positive_result == valid_data


@pytest.mark.django_db
def test_create_department(auth_client: APIClient) -> None:
    """Successfully creating a collect returns 201 and correct JSON."""
    url = reverse('collects-list')
    payload = {
        'title': 'Test_title',
        'occasion': 'other',
        'description': 'Test_description',
        'planned_amount': Decimal(1000),
        'end_date': now() + timedelta(days=5)
    }

    response = auth_client.post(url, payload, format='json')
    response_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_data['title'] == 'Test_title'
    assert 'id' in response_data

    collect = Collect.objects.get(id=response_data['id'])
    assert collect.title == 'Test_title'


@pytest.mark.django_db
def test_patch_success(collect: Collect, auth_client: APIClient) -> None:
    """Successfully partial updating a payment."""
    url = reverse('collects-detail', kwargs={'pk': collect.pk})
    payload = {
        'title': 'Update_Test_title',

    }
    response = auth_client.patch(url, payload, format='json')
    response_data = response.json()

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response_data['title'] == payload['title']
    assert response_data['title'] != collect.title


@pytest.mark.django_db
def test_patch_by_none_author(
    collect: Collect, auth_none_author_client: APIClient
) -> None:
    url = reverse('collects-detail', kwargs={'pk': collect.pk})
    payload = {
        'title': 'Update_Test_title',
    }
    response = auth_none_author_client.patch(url, payload, format='json')

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_success(collect: Collect, auth_client: APIClient) -> None:
    """Successfully delete a payment."""
    url = reverse('collects-detail', kwargs={'pk': collect.pk})
    response = auth_client.delete(url, format='json')

    assert response.status_code == HTTPStatus.NO_CONTENT
    

@pytest.mark.django_db
def test_delete_by_none_author(collect: Collect, auth_none_author_client: APIClient) -> None:
    url = reverse('collects-detail', kwargs={'pk': collect.pk})
    response = auth_none_author_client.delete(url, format='json')

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_retrieve_success(collect: Collect, auth_client: APIClient) -> None:
    url = reverse('collects-detail', kwargs={'pk': collect.pk})
    response = auth_client.get(url, format='json')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_list_success(collect_batch: CollectBatchFactory, auth_client: APIClient) -> None:
    batch_size = 25
    page_size = 10
    collect_batch(batch_size)
    url = reverse('collects-list')
    response = auth_client.get(url)
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_data['count'] == batch_size
    assert len(response_data['results']) == page_size
    assert response_data['next'] is not None