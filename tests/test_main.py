from contextlib import suppress
from runpy import run_module

from app import main


def test_main():
    assert main.main() == 0


def test_help(capfd):
    with suppress(SystemExit):
        main.main(["--help"])

    assert "usage:" in capfd.readouterr().out


def test_module_import():
    run_module("app.__main__")


def test_module_run():
    run_module("app.__main__", run_name="__main__")
