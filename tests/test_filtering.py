import pytest

from app.filtering import (
    Filter,
    FilterFactory,
    LowerFilter,
    RecordFilter,
    UpperFilter,
    register_filter,
)


@register_filter("test")
class TestFilter(Filter):
    def filter(self, value: str) -> str:
        return value + "."


def test_create_test_filter() -> None:
    test_filter = FilterFactory.create("test")
    assert isinstance(test_filter, TestFilter)


def test_create_unknown_filter() -> None:
    with pytest.raises(ValueError, match="Filter 'unknown' is unknown"):
        FilterFactory.create("unknown")


def test_create_record_filter() -> None:
    record_filter = FilterFactory.create_record_filter(
        {
            "a": (),
            "b": ("test",),
        }
    )

    assert len(record_filter.filters["a"]) == 0
    assert len(record_filter.filters["b"]) == 1
    assert isinstance(record_filter.filters["b"][0], TestFilter)


def test_record_filter() -> None:
    record_filter = RecordFilter({"field": (TestFilter(), TestFilter())})
    filtered = record_filter.filter({"field": "value"})
    assert filtered == {"field": "value.."}


def test_lower_filter() -> None:
    lower = LowerFilter()
    assert isinstance(lower, Filter)
    assert lower.filter("ABC") == "abc"


def test_upper_filter() -> None:
    upper = UpperFilter()
    assert isinstance(upper, Filter)
    assert upper.filter("abc") == "ABC"
