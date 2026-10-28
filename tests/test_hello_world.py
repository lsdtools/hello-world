"""The package's pipeline, run headless: the shape step doubles every value.

    lsdtools python tests/test_hello_world.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lsdtools import Engine, Source, Table  # noqa: E402

from lsdtools_hello_world.tool import double, rows  # noqa: E402


def test_the_shape_step_doubles_x():
    csv = os.path.join(tempfile.mkdtemp(), "numbers.csv")
    Table({"x": [1, 2, 3]}).write_csv(csv)
    result = Engine().run(double(t=rows(src=Source.file(csv)))).raise_on_error()
    assert [row["x"] for row in result.output.to_pylist()] == [2, 4, 6]


if __name__ == "__main__":
    test_the_shape_step_doubles_x()
    print("ok")
