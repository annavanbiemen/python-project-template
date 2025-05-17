from pytest import CaptureFixture
from app.main import main


def test_main(capfd: CaptureFixture[str]) -> None:
    main()
    assert capfd.readouterr().out == "Hello World!\n"
