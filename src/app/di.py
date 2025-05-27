from csv import DictReader, DictWriter
from pathlib import Path
from sys import stdin, stdout
from typing import IO

from . import app, config, filtering, io


class Container:
    def __init__(self, configuration: config.Configuration) -> None:
        self.config = configuration

    def input(self) -> IO:
        if self.config.input is None:
            return stdin
        return Path(self.config.input).open(encoding="utf-8-sig")

    def reader(self, file: IO) -> DictReader[str]:
        return DictReader(file, delimiter=";")

    def reader_context(self) -> io.ContextualFactory[DictReader[str]]:
        return io.ContextualFactory(self.input(), self.reader)

    def output(self) -> IO:
        if self.config.output is None:
            return stdout
        return Path(self.config.output).open("w", encoding="utf-8-sig")

    def writer(self, file: IO) -> DictWriter[str]:
        return DictWriter(file, fieldnames=self.config.get_field_names())

    def writer_context(self) -> io.ContextualFactory[DictWriter[str]]:
        return io.ContextualFactory(self.output(), self.writer)

    def record_filter(self) -> filtering.RecordFilter:
        return filtering.FilterFactory.create_record_filter(
            self.config.get_field_filters()
        )

    def application(self) -> app.Application:
        return app.Application(
            reader_context=self.reader_context(),
            writer_context=self.writer_context(),
            record_filter=self.record_filter(),
        )
