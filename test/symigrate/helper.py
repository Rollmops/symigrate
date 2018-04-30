import textwrap


def dedent_and_remove_white_lines(text: str) -> str:
    return_text = textwrap.dedent(text).lstrip("\n")

    return return_text
