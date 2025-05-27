import contextlib
import sys
from io import StringIO
from runpy import run_module

import pytest

from app.main import main


def test_help(capfd: pytest.CaptureFixture[str]) -> None:
    with contextlib.suppress(SystemExit):
        main(["--help"])

    assert "usage:" in capfd.readouterr().out


def test_csvfilter(mocker) -> None:
    output = StringIO()
    mocker.patch("app.di.stdin", new=StringIO("Column\nValue1\nValue2\n"))
    mocker.patch("app.di.stdout", new=output)

    main(["Column"])

    assert output.getvalue() == "Column\r\nValue1\r\nValue2\r\n"


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
