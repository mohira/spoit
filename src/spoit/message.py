import click
import pandas as pd


def csv_info_message(cols: pd.Index, csv_filename: str) -> str:
    return f'{csv_filename}({len(cols)} cols)\n{cols.tolist()}\n'


def mode_message(all_unused: bool, omit: bool) -> str:
    if all_unused:
        return click.style(f'all unused mode: copy all cols as comment\n', fg='yellow')
    elif omit:
        return click.style('omit mode: not copy unused cols\n', fg='red')
    else:
        return click.style('no omit mode: copy unused cols with # \n', fg='green')
