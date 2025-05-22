from collections.abc import Callable
from typing import Generic, IO, TypeVar


T = TypeVar("T")


class ContextualFactory(Generic[T]):
    """Delegates context management while creating an IO-consuming service."""

    def __init__(self, stream: IO, factory: Callable[[IO], T]) -> None:
        self.stream = stream
        self.factory = factory

    def __enter__(self) -> T:
        return self.factory(self.stream.__enter__())

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stream.__exit__(exc_type, exc_val, exc_tb)
