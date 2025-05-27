import contextlib
import sys
from runpy import run_module

import pytest

from app.main import main


def test_help(capfd: pytest.CaptureFixture[str]) -> None:
    with contextlib.suppress(SystemExit):
        main(["--help"])

    assert "usage:" in capfd.readouterr().out


def test_module_import(monkeypatch) -> None:
    def do_not_call() -> None:
        raise RuntimeError

    monkeypatch.setattr(sys.modules['app.main'], "main", do_not_call)
    run_module("app.__main__")


def test_module_run(monkeypatch, mocker) -> None:
    mock = mocker.Mock()

    monkeypatch.setattr(sys.modules['app.main'], "main", mock)
    run_module("app.__main__", run_name="__main__")

    assert mock.call_count == 1
