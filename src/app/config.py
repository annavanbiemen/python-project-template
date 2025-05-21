import dataclasses
import os


@dataclasses.dataclass
class Configuration:
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

    def get_field_names(self) -> tuple[str, ...]:
        return tuple(field.split(".")[0] for field in self.fields)

    def get_field_filters(self) -> dict[str, tuple[str, ...]]:
        return {
            field[0]: tuple(field[1:])
            for field in (field.split(".") for field in self.fields)
        }
