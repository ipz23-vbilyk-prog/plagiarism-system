import re


def highlight_matches_pdf(text, matches):
    for m in matches:
        fragment = m["fragment"]

        text = text.replace(
            fragment,
            f'<font color="red">{fragment}</font>'
        )

    return text