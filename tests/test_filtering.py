from app.filtering import Filter, LowerFilter, UpperFilter


def test_lower_filter() -> None:
    lower = LowerFilter()
    assert isinstance(lower, Filter)
    assert lower.filter("ABC") == "abc"


def test_upper_filter() -> None:
    upper = UpperFilter()
    assert isinstance(upper, Filter)
    assert upper.filter("abc") == "ABC"
