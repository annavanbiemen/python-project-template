from . import filtering, io


class Application:
    def __init__(
        self,
        reader_context: io.ReaderContext,
        writer_context: io.WriterContext,
        record_filter: filtering.RecordFilter,
    ):
        self.reader_context = reader_context
        self.writer_context = writer_context
        self.record_filter = record_filter

    def run(self):
        with self.reader_context as reader, self.writer_context as writer:
            writer.writeheader()
            for record in reader:
                writer.writerow(self.record_filter.filter(record))
