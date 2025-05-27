from csv import DictReader, DictWriter
from pathlib import Path
from sys import stdin, stdout
from typing import IO

from . import app, config, filtering, io


class Container:
    """Simple DI container with service definitions in functions."""

    def __init__(self, configuration: config.Configuration) -> None:
        """Initialize container."""
        self.config = configuration

    def input(self) -> IO:
        """Create IO input stream from input file (or return sys.stdin)."""
        if self.config.input is None:
            return stdin
        return Path(self.config.input).open(encoding="utf-8-sig")

    def reader(self, file: IO) -> DictReader[str]:
        """Create reader from opened file."""
        return DictReader(file, delimiter=";")

    def reader_context(self) -> io.ContextualFactory[DictReader[str]]:
        """Create contextual factory with opened file and reader factory."""
        return io.ContextualFactory(self.input(), self.reader)

    def output(self) -> IO:
        """Create IO output stream from output file (or return sys.stdout)."""
        if self.config.output is None:
            return stdout
        return Path(self.config.output).open("w", encoding="utf-8-sig")

    def writer(self, file: IO) -> DictWriter[str]:
        """Create writer from opened file."""
        return DictWriter(file, fieldnames=self.config.get_field_names())

    def writer_context(self) -> io.ContextualFactory[DictWriter[str]]:
        """Create contextual factory with opened file and writer factory."""
        return io.ContextualFactory(self.output(), self.writer)

    def record_filter(self) -> filtering.RecordFilter:
        """Create record filter based on configuration."""
        return filtering.FilterFactory.create_record_filter(
            self.config.get_field_filters()
        )

    def application(self) -> app.Application:
        """Create application."""
        return app.Application(
            reader_context=self.reader_context(),
            writer_context=self.writer_context(),
            record_filter=self.record_filter(),
        )
