import csv
import sys
from typing import IO
from collections.abc import Callable


class ReaderContext:
    def __init__(
        self,
        input_factory: Callable[[], IO],
        reader_factory: Callable[[IO], csv.DictReader[str]],
    ):
        self.file: IO | None
        self.input_factory = input_factory
        self.reader_factory = reader_factory

    def __enter__(self) -> csv.DictReader[str]:
        self.file = self.input_factory()

        return self.reader_factory(self.file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file not in (None, sys.stdin):
            self.file.close()


class WriterContext:
    def __init__(
        self,
        output_factory: Callable[[], IO],
        writer_factory: Callable[[IO], csv.DictWriter[str]],
    ):
        self.file: IO | None
        self.output_factory = output_factory
        self.writer_factory = writer_factory

    def __enter__(self) -> csv.DictWriter[str]:
        self.file = self.output_factory()

        return self.writer_factory(self.file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file not in (None, sys.stdout):
            self.file.close()
