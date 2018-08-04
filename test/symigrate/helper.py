import sys
import textwrap
from contextlib import contextmanager
from io import StringIO


def dedent_and_remove_first_empty_line(text: str) -> str:
    return_text = textwrap.dedent(text).lstrip("\n")

    return return_text


@contextmanager
def capture_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
