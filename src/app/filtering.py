from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping
from typing import ClassVar


class Filter(ABC):
    """Abstract filter base class."""

    @abstractmethod
    def filter(self, value: str) -> str:  # pragma: no cover
        """Filter value."""
        raise NotImplementedError


class ValueFilter(Filter):
    """Value filter."""

    def __init__(self, filters: Iterable[Filter]) -> None:
        """Initialize value filter."""
        self.filters = filters

    def filter(self, value: str) -> str:
        """Filter value."""
        for filter_instance in self.filters:
            value = filter_instance.filter(value)

        return value


class RecordFilter:
    """Record filter."""

    def __init__(self, filters: dict[str, ValueFilter]) -> None:
        """Initialize record filter."""
        self.filters = filters

    def filter(self, record: dict[str, str]) -> dict[str, str]:
        """Filter record."""
        return {
            field: value_filter.filter(record[field])
            for field, value_filter in self.filters.items()
        }


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
    def create_value_filter(cls, names: Iterable[str]) -> ValueFilter:
        """Create a filter instance by name."""
        return ValueFilter([cls.create(name) for name in names])

    @classmethod
    def create_record_filter(
        cls, field_filters: Mapping[str, Iterable[str]]
    ) -> RecordFilter:
        """Create a record filter using a mapping of field names to filters."""
        return RecordFilter(
            {
                field: cls.create_value_filter(names)
                for field, names in field_filters.items()
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
