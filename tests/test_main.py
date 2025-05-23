from runpy import run_module
from pytest import CaptureFixture
from runpy import run_module
from app.main import main


def test_main(capfd: CaptureFixture[str]) -> None:
    assert main() == 0
    assert capfd.readouterr().out == "Hello World!\n"


def test_help(capfd: CaptureFixture[str]) -> None:
    try:
        main(["--help"])
    except SystemExit:
        pass

    assert "usage:" in capfd.readouterr().out


def test_module_import() -> None:
    run_module("app.__main__")


def test_module_run() -> None:
    run_module("app.__main__", run_name="__main__")
