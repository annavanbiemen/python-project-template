from collections.abc import Callable
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Generic, TextIO, TypeVar

T = TypeVar("T")


class ContextualFactory(Generic[T]):
    """Delegates context management while creating an IO-consuming service."""

    def __init__(
        self,
        stream: AbstractContextManager[TextIO],
        factory: Callable[[TextIO], T],
    ) -> None:
        """Initialize contextual factory."""
        self.stream = stream
        self.factory = factory

    def __enter__(self) -> T:
        """Delegate entering context and create service."""
        return self.factory(self.stream.__enter__())

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: TracebackType | None,
    ) -> None:
        """Delegate exiting context."""
        self.stream.__exit__(
            exception_type,
            exception_value,
            exception_traceback,
        )
