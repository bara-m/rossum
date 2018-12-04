import json
from io import StringIO

from click.testing import CliRunner
import pandas as pd

from tools import xls_to_csv


FILENAME = "some.xls"
DATA = """\
1;abc
2;cde
3;fgh\
"""


class TestXLSToCSV:
    def test_success(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with StringIO() as csv, open(FILENAME, "wb") as xls:
                csv.write(DATA)
                csv.seek(0)
                df = pd.read_csv(
                    csv, sep=";", names=["value", "label"], header=None, dtype=(str, str)
                )
                df.to_excel(xls, index=False)

            result = runner.invoke(xls_to_csv.cli, [FILENAME, "--header", "0"])
        assert not result.exit_code
        assert DATA == result.stdout.strip()