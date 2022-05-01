from pathlib import Path

import pandas as pd
import pytest
from pandas.errors import EmptyDataError
from pandas.testing import assert_index_equal

from src.spoit.main import get_cols


class TestMain:
    @pytest.fixture()
    def testdata_path(self) -> Path:
        return Path(__file__).parent / 'testdata'

    class TestGetCols:
        def test_get_cols(self, testdata_path: Path):
            csv_path = testdata_path / 'users.csv'
            cols = get_cols(csv_path)

            want = pd.Index(['name', 'age', 'email', 'address', 'phone'])

            assert_index_equal(cols, want)

        def test_csv_must_be_not_empty(self, testdata_path: Path):
            csv_path = testdata_path / 'empty.csv'

            with pytest.raises(EmptyDataError):
                get_cols(csv_path)
