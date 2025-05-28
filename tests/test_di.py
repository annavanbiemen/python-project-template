from contextlib import nullcontext
from sys import stdin, stdout

from app.config import Configuration
from app.di import Container


def create_container(**kwargs) -> Container:
    return Container(Configuration(**kwargs))


def test_input_stdin() -> None:
    container = create_container(input=None)
    input_context = container.input()
    assert isinstance(input_context, nullcontext)
    assert input_context.__enter__() is stdin


def test_input_file(fs) -> None:
    fs.create_file("/fake/input.csv", contents="content")
    container = create_container(input="/fake/input.csv")
    with container.input() as input_stream:
        assert input_stream.read() == "content"


def test_output_stdout() -> None:
    container = create_container(output=None)
    output_context = container.output()
    assert isinstance(output_context, nullcontext)
    assert output_context.__enter__() is stdout


def test_output_file(fs) -> None:
    container = create_container(output="/output.csv")
    with container.output() as output_stream:
        output_stream.write("content")
    assert fs.get_object("/output.csv").contents == "content"
