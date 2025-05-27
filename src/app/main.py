from argparse import ArgumentParser

from . import config, di


def main(args: list[str] | None = None) -> int:
    """CSVFilter Main function."""
    configuration = config.Configuration()

    parser = ArgumentParser("app")
    parser.add_argument("-i", "--input", help="Read from INPUT file")
    parser.add_argument("-o", "--output", help="Write to OUTPUT file")
    parser.add_argument(
        "fields",
        nargs="*",
        default=configuration.fields,
        help="Fields in name.filter1.filter2 format",
    )
    parser.parse_args(args, configuration)

    container = di.Container(configuration)
    container.application().run()

    return 0
