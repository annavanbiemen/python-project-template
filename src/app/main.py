import argparse


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser("app")
    parser.parse_args(args)

    print("Hello World!")

    return 0
