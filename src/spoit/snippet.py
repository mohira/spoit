import pandas as pd


def build_snippet(cols: pd.Index, usecols_or_not: list[bool], csv_path: str, omit: False) -> str:
    snippet = 'usecols = [\n'

    if omit:
        usecols = cols[usecols_or_not]
        each_cols = [f"\t'{col}'," for col in usecols]
    else:
        each_cols = []
        for idx, use in enumerate(usecols_or_not):
            col = cols[idx]
            if use:
                each_cols.append(f"\t'{col}',")
            else:
                each_cols.append(f"\t# '{col}',")

    body = '\n'.join(each_cols)

    snippet += body
    snippet += '\n]\n'

    snippet += f"df = pd.read_csv('{csv_path}', usecols=usecols)\n"

    return snippet
