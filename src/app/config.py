from dataclasses import dataclass, field
from os import getenv


@dataclass
class Configuration:
    """Configuration settings."""

    input: str | None = getenv("CSVFILTER_INPUT")
    output: str | None = getenv("CSVFILTER_OUTPUT")
    fields: list[str] = field(
        default_factory=lambda: list(
            filter(
                len,
                getenv("CSVFILTER_FIELDS", "").split(","),
            )
        )
    )
    """Fields as a list of strings in 'field.filter1.filter2' format."""

    def get_field_names(self) -> tuple[str, ...]:
        """Get a list of field name strings."""
        return tuple(parts.split(".")[0] for parts in self.fields)

    def get_field_filters(self) -> dict[str, tuple[str, ...]]:
        """Get a dictionary of field names with filter name tuples."""
        return {
            part[0]: tuple(part[1:])
            for part in (parts.split(".") for parts in self.fields)
        }
