from collections.abc import Callable
from types import TracebackType
from typing import IO, Generic, TypeVar

T = TypeVar("T")


class ContextualFactory(Generic[T]):
    """Delegates context management while creating an IO-consuming service."""

    def __init__(self, stream: IO, factory: Callable[[IO], T]) -> None:
        self.stream = stream
        self.factory = factory

    def __enter__(self) -> T:
        return self.factory(self.stream.__enter__())

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: TracebackType | None,
    ) -> None:
        self.stream.__exit__(
            exception_type,
            exception_value,
            exception_traceback,
        )
