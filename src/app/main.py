import argparse


def main(args: list[str] | None = None) -> int:
    """Run the application."""
    parser = argparse.ArgumentParser("app")
    parser.parse_args(args)

    # ...

    return 0
