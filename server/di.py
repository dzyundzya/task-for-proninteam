import punq
from django.conf import LazySettings, settings


def _inject_settings(container: punq.Container) -> None:
    """Register settings."""
    container.register(LazySettings, instance=settings, scope='singleton')


def _injest_infra(container: punq.Container) -> None:
    """Register repositories."""
    pass


def create_container() -> punq.Container:
    """Create container."""
    container = punq.Container()
    _inject_settings(container)
    _injest_infra(container)
    return container


def resolve[Thing](thing: type[Thing]) -> Thing:
    """Resolve thing dependencies."""
    return container.resolve(thing)  # type: ignore[no-any-return]


container = create_container()
