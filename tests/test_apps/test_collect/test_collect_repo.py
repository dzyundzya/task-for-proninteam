import pytest

from server.apps.collects.infra.repository import CollectRepo
from server.apps.collects.models import Collect
from server.di import resolve
from tests.plugins.collects import CollectBatchFactory


@pytest.mark.django_db
def test_get_all(collect_batch: CollectBatchFactory) -> None:
    """Test the `get_all()` method of CollectRepo."""
    batch_size = 3
    collect_batch(batch_size)

    repo = resolve(CollectRepo)
    all_collects = repo.get_all()

    assert all_collects.count() == batch_size


@pytest.mark.django_db
def test_get_by_pk(collect: Collect) -> None:
    """Test the `get_by_pk()` method of CollectRepo."""
    repo = resolve(CollectRepo)
    collect_obj = repo.get_by_pk(pk=collect.id)

    assert collect_obj == collect


@pytest.mark.django_db
def test_get_by_pk_none() -> None:
    """get_by_pk raises Collect.DoesNotExist if object is missing."""
    repo = resolve(CollectRepo)
    with pytest.raises(Collect.DoesNotExist):
        repo.get_by_pk(pk=1)


@pytest.mark.django_db
def test_get_all_active_collects(collect: Collect) -> None:
    """Test the `get_all_active()` method of CollectRepo."""
    repo = resolve(CollectRepo)
    collect_non_active = collect
    collect_non_active.is_active = False
    all_active_collect = repo.get_all_active()
    all_collect = repo.get_all()

    assert all_collect != all_active_collect
