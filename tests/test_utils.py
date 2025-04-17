from pathlib import Path

from leolino_kids_prio.utils import Data


def test_good():
    d = Data(Path(__file__).parent / "test_data_good")
    tmp = d.allowed_and_prio("U3", ["F", "A"])
