from pathlib import Path

from leolino_kids_prio.utils import Data


def test_good():
    d = Data(Path(__file__).parent / "test_data_good")
    assert isinstance(d.always_allowed_kids, dict)

    result = d.allowed_and_prio("U3", ["F", "A"])
    assert result == (
        ["Holly", "Luca", "Khan", "Giulio", "Leia", "Lian"],
        4,
        [
            "Thomas",
            "Viola",
            "Emilia",
            "Ava",
            "Emma",
            "Constantin",
            "Tino",
            "Robert",
            "Marissa",
            "Lisa",
            "Adya",
            "Aaron",
        ],
    )
