import dataclasses
import os


@dataclasses.dataclass
class Configuration:
    """Configuration settings."""

    input: str | None = os.getenv("CSVFILTER_INPUT")
    output: str | None = os.getenv("CSVFILTER_OUTPUT")
    fields: list[str] = dataclasses.field(
        default_factory=lambda: list(
            filter(
                len,
                os.getenv("CSVFILTER_FIELDS", "").split(","),
            )
        )
    )
    """Fields as a list of strings in 'field.filter1.filter2' format."""

    def get_field_names(self) -> tuple[str, ...]:
        """Get list of field name strings."""
        return tuple(field.split(".")[0] for field in self.fields)

    def get_field_filters(self) -> dict[str, tuple[str, ...]]:
        """Get dictionary of field name, filter name tuples."""
        return {
            field[0]: tuple(field[1:])
            for field in (field.split(".") for field in self.fields)
        }
