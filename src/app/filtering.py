from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import ClassVar


class Filter(ABC):
    @abstractmethod
    def filter(self, value: str) -> str:
        raise NotImplementedError


class RecordFilter:
    def __init__(self, filters: dict[str, tuple[Filter, ...]]) -> None:
        self.filters = filters

    def filter(self, record: dict[str, str]) -> dict[str, str]:
        result = {}
        for field, filters in self.filters.items():
            value = record[field]
            for filter_instance in filters:
                value = filter_instance.filter(value)

            result[field] = value

        return result


class FilterFactory:
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
        return RecordFilter(
            {
                field: tuple(cls.create(name) for name in filters)
                for field, filters in field_filters.items()
            }
        )


def register_filter(name: str) -> Callable[[type[Filter]], type[Filter]]:
    def decorator(cls: type[Filter]) -> type[Filter]:
        FilterFactory.register(name, cls)
        return cls

    return decorator


@register_filter("upper")
class UpperFilter(Filter):
    def filter(self, value: str) -> str:
        return value.upper()


@register_filter("lower")
class LowerFilter(Filter):
    """Returns lowercased value."""

    def filter(self, value: str) -> str:
        return value.lower()
