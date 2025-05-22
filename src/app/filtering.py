from abc import abstractmethod, ABC


class Filter(ABC):
    @abstractmethod
    def filter(self, value: str) -> str:
        raise NotImplementedError


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


class FilterFactory:
    _filters: dict[str, type[Filter]] = {}

    @classmethod
    def register(cls, name: str, filter_class: type[Filter]) -> None:
        """Register a filter class by name."""
        cls._filters[name] = filter_class

    @classmethod
    def create(cls, name: str) -> Filter:
        """Create a filter instance by name."""
        filter_class = cls._filters.get(name)
        if filter_class is None:
            raise ValueError(f"Filter '{name}' is unknown.")

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


class UpperFilter(Filter):
    def filter(self, value: str) -> str:
        return value.upper()


class LowerFilter(Filter):
    def filter(self, value: str) -> str:
        return value.lower()


FilterFactory.register("upper", UpperFilter)
FilterFactory.register("lower", LowerFilter)
