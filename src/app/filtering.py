from abc import abstractmethod, ABC
import sys


class Filter(ABC):
    @abstractmethod
    def filter(self, value: str) -> str:
        raise NotImplementedError

    @staticmethod
    def create(filter_name: str) -> "Filter":
        filter_class_name = filter_name.capitalize() + "Filter"
        filter_class = getattr(sys.modules[__name__], filter_class_name)

        assert filter_class is not None, f"Unknown filter: {filter_name}"
        assert issubclass(filter_class, Filter), f"Not a filter: {filter_name}"

        return filter_class()


class RecordFilter:
    def __init__(self, filters: dict[str, tuple[Filter, ...]]):
        self.filters = filters

    def filter(self, record: dict[str, str]) -> dict[str, str]:
        result = {}
        for field, filters in self.filters.items():
            value = record[field]
            for filter_instance in filters:
                value = filter_instance.filter(value)

            result[field] = value

        return result

    @classmethod
    def create(cls, field_filters: dict[str, tuple[str, ...]]):
        return cls(
            {
                field: tuple(Filter.create(name) for name in filters)
                for field, filters in field_filters.items()
            }
        )


class UpperFilter(Filter):
    def filter(self, value: str) -> str:
        return value.upper()


class LowerFilter(Filter):
    def filter(self, value: str) -> str:
        return value.lower()
