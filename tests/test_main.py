import contextlib
from runpy import run_module

import pytest

from app.main import main


def test_help(capfd: pytest.CaptureFixture[str]) -> None:
    with contextlib.suppress(SystemExit):
        main(["--help"])

    assert "usage:" in capfd.readouterr().out


def test_module_import() -> None:
    run_module("app.__main__")


def test_module_run() -> None:
    run_module("app.__main__", run_name="__main__")
