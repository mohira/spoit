from pathlib import Path

import pytest

from src.spoit.main import get_cols
from src.spoit.snippet import build_snippet


class TestSnippet:

    @pytest.fixture()
    def testdata_path(self) -> Path:
        return Path(__file__).parent / 'testdata'

    @pytest.mark.parametrize('omit, golden_filename', [
        pytest.param(True, 'omit.py', id='omit'),
        pytest.param(False, 'no_omit.py', id='no-omit'),
    ])
    def test_build_snippet(self, omit: bool, golden_filename: str, testdata_path: Path):
        csv_path = testdata_path / 'users.csv'
        cols = get_cols(csv_path)

        actual = build_snippet(cols, [True, True, True, False, False], csv_path.name, omit)

        want = (testdata_path / golden_filename).read_text()

        assert actual == want
