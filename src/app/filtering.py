from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import ClassVar


class Filter(ABC):
    """Abstract filter base class."""

    @abstractmethod
    def filter(self, value: str) -> str:  # pragma: no cover
        """Filter value."""
        raise NotImplementedError


class RecordFilter:
    """Record filter."""

    def __init__(self, filters: dict[str, tuple[Filter, ...]]) -> None:
        """Initialize record filter."""
        self.filters = filters

    def filter(self, record: dict[str, str]) -> dict[str, str]:
        """Filter record."""
        result = {}
        for field, filters in self.filters.items():
            value = record[field]
            for filter_instance in filters:
                value = filter_instance.filter(value)

            result[field] = value

        return result


class FilterFactory:
    """Filter factory for creating filters by their registered name."""

    _filters: ClassVar[dict[str, type[Filter]]] = {}

    @classmethod
    def register(cls, name: str, filter_class: type[Filter]) -> None:
        """Register a filter class by name."""
        cls._filters[name] = filter_class

    @classmethod
    def create(cls, name: str) -> Filter:
        """Create a filter instance by name."""
        filter_class = cls._filters.get(name)
        if filter_class is None:
            msg = f"Filter '{name}' is unknown."
            raise ValueError(msg)

        return filter_class()

    @classmethod
    def create_record_filter(
        cls, field_filters: dict[str, tuple[str, ...]]
    ) -> RecordFilter:
        """Create a record filter using a dict of field names and filters."""
        return RecordFilter(
            {
                field: tuple(cls.create(name) for name in filters)
                for field, filters in field_filters.items()
            }
        )


def register_filter(name: str) -> Callable[[type[Filter]], type[Filter]]:
    """Register a named filter with the filter factory."""

    def decorator(cls: type[Filter]) -> type[Filter]:
        FilterFactory.register(name, cls)
        return cls

    return decorator


@register_filter("upper")
class UpperFilter(Filter):
    """Upper filter."""

    def filter(self, value: str) -> str:
        """Apply upper filter."""
        return value.upper()


@register_filter("lower")
class LowerFilter(Filter):
    """Lower filter."""

    def filter(self, value: str) -> str:
        """Apply lower filter."""
        return value.lower()
