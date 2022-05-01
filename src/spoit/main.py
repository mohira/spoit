from pathlib import Path

import click
import pandas as pd
import pyperclip
from pandas.errors import EmptyDataError

from .snippet import build_snippet


def prompt_usecols_or_not(cols: pd.Index) -> list[bool]:
    bool_indexes = []

    for idx, col in enumerate(cols, start=1):
        msg = f'({idx}/{len(cols)}) "' + click.style(f'{col}', fg='yellow') + '"?'

        use_or_not: bool = click.confirm(msg)

        bool_indexes.append(use_or_not)

    return bool_indexes


def retry_message(cols: pd.Index, usecols_or_not: list[bool]) -> str:
    usecols = cols[usecols_or_not].tolist()

    if len(usecols) == 0:
        return '\nYou chose 0 cols, please retry'

    if click.confirm(f'\nYou chose ' + click.style(f'{usecols}', fg='yellow') + ' Retry?'):
        return 'OK, please retry'

    return ''


def get_cols(p: Path) -> pd.Index:
    with p.open() as f:
        if f.readline() == '':
            raise EmptyDataError(f'{p} is empty. No columns to parse from file')

    return pd.read_csv(p, nrows=0).columns


@click.command()
@click.argument('csv-path', type=click.Path(exists=True))
@click.option('--omit/--no-omit', default=False, help='omit unused cols')
@click.option('--all-unused', '-a', is_flag=True, default=False, help='copy all unused cols as comment')
def main(csv_path: str, omit: bool, all_unused: bool):
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
    p = Path(csv_path)
    if (not p.is_file()) or (p.suffix != '.csv'):
        raise click.UsageError(f'{csv_path} is not CSV.')

    try:
        cols = get_cols(p)
    except EmptyDataError as e:
        raise click.UsageError(f'{e}')

    click.echo(f'{csv_path}({len(cols)} cols)\n{cols.tolist()}\n')

    if all_unused:
        snippet = build_snippet(cols, [False for _ in range(len(cols))], csv_path, omit=False)

        pyperclip.copy(snippet)
        click.echo(click.style(f'👍Copied all unused cols as comment to your clipboard', fg='yellow'))

        exit(0)

    if omit:
        click.echo(click.style('omit mode: not copy unused cols\n', fg='red'))
    else:
        click.echo(click.style('no omit mode: copy unused cols with # \n', fg='green'))

    usecols_or_not = prompt_usecols_or_not(cols)
    while msg := retry_message(cols, usecols_or_not):
        click.echo(msg)
        usecols_or_not = prompt_usecols_or_not(cols)

    snippet = build_snippet(cols, usecols_or_not, csv_path, omit)

    pyperclip.copy(snippet)
    click.echo(click.style(f'👍Copied the snippet to your clipboard', fg='green'))


if __name__ == '__main__':
    main()
