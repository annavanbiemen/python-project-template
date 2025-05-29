from behave import given, when, then
from io import StringIO

from app import di, main


@given('the following input')
def step_impl(context):
    context.input = context.text


@given('the field "{field}"')
def step_impl(context, field: str):
    context.fields = [field]


@when('I run the CSV filter')
def step_impl(context):
    stdin = di.stdin
    stdout = di.stdout
    try:
        di.stdin = StringIO(context.input)
        di.stdout = StringIO()
        main.main(context.fields)
        context.output = di.stdout.getvalue()
    finally:
        di.stdin = stdin
        di.stdout = stdout


@then('the output should be')
def step_impl(context):
    actual = context.output.strip().replace("\r\n", "\n")
    expected = context.text.strip().replace("\r\n", "\n")
    assert actual == expected, f"Expected:\n{expected}\nActual:\n{actual}"
