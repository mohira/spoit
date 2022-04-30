from pathlib import Path

import pandas as pd
import pytest

from spoit.snippet import build_snippet


class TestSnippet:

    @pytest.mark.parametrize('csv_path, bool_indexes, omit, want', [
        pytest.param('./testdata/users.csv',
                     [True, True, True, False, False], True, Path('./testdata/omit.py').read_text(), id='omit'),
        pytest.param('./testdata/users.csv',
                     [True, True, True, False, False], False, Path('./testdata/no_omit.py').read_text(), id='no omit'),
    ])
    def test_build_snippet(self, csv_path: str, bool_indexes: list[bool], omit: bool, want: str):
        actual = build_snippet(pd.read_csv(csv_path).columns, bool_indexes, csv_path, omit)

        assert actual == want
