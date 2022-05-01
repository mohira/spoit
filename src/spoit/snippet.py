import pandas as pd

template = """usecols = [
{body}
]
df = pd.read_csv('{filename}', usecols=usecols)
"""


def build_snippet(cols: pd.Index, usecols_or_not: list[bool], filename: str, omit: False) -> str:
    each_cols = _each_cols(cols, usecols_or_not, omit)

    body = '\n'.join(each_cols)

    return template.format(body=body, filename=filename)


def _each_cols(cols: pd.Index, usecols_or_not: list[bool], omit: bool) -> list[str]:
    if omit:
        return [f"\t'{col}'," for col in cols[usecols_or_not]]

    return [f"\t'{col}'," if use else f"\t# '{col}'," for use, col in zip(usecols_or_not, cols)]
