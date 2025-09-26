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
