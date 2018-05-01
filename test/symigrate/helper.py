import textwrap


def dedent_and_remove_first_empty_line(text: str) -> str:
    return_text = textwrap.dedent(text).lstrip("\n")

    return return_text
