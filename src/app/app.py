from csv import DictReader, DictWriter

from . import filtering, io


class Application:
    """CSVFilter application."""

    def __init__(
        self,
        reader_context: io.ContextualFactory[DictReader[str]],
        writer_context: io.ContextualFactory[DictWriter[str]],
        record_filter: filtering.RecordFilter,
    ) -> None:
        """Initialize Application properties."""
        self.reader_context = reader_context
        self.writer_context = writer_context
        self.record_filter = record_filter

    def run(self) -> None:
        """Read, filter and write all records iteratively."""
        with self.reader_context as reader, self.writer_context as writer:
            writer.writeheader()
            for record in reader:
                writer.writerow(self.record_filter.filter(record))
