from pytest import CaptureFixture
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
