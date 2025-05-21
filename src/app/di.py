import csv
import sys
from typing import IO
from . import app, config, filtering, io


class Container:
    def __init__(self, configuration: config.Configuration) -> None:
        self.config = configuration

    def input(self) -> IO:
        if self.config.input is None:
            return sys.stdin
        return open(self.config.input, "r", encoding="utf-8-sig")

    def reader(self, file: IO) -> csv.DictReader[str]:
        return csv.DictReader(file, delimiter=";")

    def reader_context(self) -> io.ReaderContext:
        return io.ReaderContext(self.input, self.reader)

    def output(self) -> IO:
        if self.config.output is None:
            return sys.stdout
        return open(self.config.output, "w", encoding="utf-8-sig")

    def writer(self, file: IO) -> csv.DictWriter[str]:
        return csv.DictWriter(file, fieldnames=self.config.get_field_names())

    def writer_context(self) -> io.WriterContext:
        return io.WriterContext(self.output, self.writer)

    def record_filter(self) -> filtering.RecordFilter:
        return filtering.RecordFilter.create(self.config.get_field_filters())

    def application(self) -> app.Application:
        return app.Application(
            reader_context=self.reader_context(),
            writer_context=self.writer_context(),
            record_filter=self.record_filter(),
        )
