from pathlib import Path

import click
import pandas as pd
import pyperclip
from pandas.errors import EmptyDataError

from spoit.message import csv_info_message, mode_message
from .snippet import build_snippet


def prompt_usecols_or_not(cols: pd.Index) -> list[bool]:
    usecols_or_not = []

    for idx, col in enumerate(cols, start=1):
        msg = f'({idx}/{len(cols)}) "' + click.style(f'{col}', fg='yellow') + '"?'

        usecols_or_not.append(click.confirm(msg))

    return usecols_or_not


def get_cols(p: Path) -> pd.Index:
    with p.open() as f:
        if f.readline() == '':
            raise EmptyDataError(f'{p} is empty. No columns to parse from file')

    return pd.read_csv(p, nrows=0).columns


@click.command()
@click.argument('csv-filename', type=click.Path(exists=True))
@click.option('--all-unused', '-a', is_flag=True, default=False, help='copy all unused cols as comment')
@click.option('--omit/--no-omit', default=False, help='omit unused cols')
def main(csv_filename: str, all_unused: bool, omit: bool):
    """spoit: Create a snippet to extract col from csv.

    example: You choose ['name', 'email', 'phone'] from users.csv, get the below snippet.

    \b
    usecols = [
	'name',
	# 'age',
	'email',
	# 'address',
	'phone',
    ]
    df = pd.read_csv('users.csv', usecols=usecols)
    """
    csv_path = Path(csv_filename)
    if (not csv_path.is_file()) or (csv_path.suffix != '.csv'):
        raise click.UsageError(f'{csv_filename} is not CSV.')

    try:
        cols = get_cols(csv_path)
    except EmptyDataError as e:
        raise click.UsageError(f'{e}')

    click.echo(csv_info_message(cols, csv_filename))

    click.echo(mode_message(all_unused, omit))

    if all_unused:
        usecols_or_not = [False for _ in range(len(cols))]
    else:
        usecols_or_not = prompt_usecols_or_not(cols)
        usecols = cols[usecols_or_not].tolist()

        while click.confirm(f'\nYou chose ' + click.style(f'{usecols}', fg='yellow') + ' Retry?'):
            click.echo('OK, please retry')
            usecols_or_not = prompt_usecols_or_not(cols)
            usecols = cols[usecols_or_not].tolist()

    snippet = build_snippet(cols, usecols_or_not, csv_filename, omit)
    pyperclip.copy(snippet)

    click.echo(click.style(f'👍Copied the snippet to your clipboard', fg='green'))


if __name__ == '__main__':
    main()
