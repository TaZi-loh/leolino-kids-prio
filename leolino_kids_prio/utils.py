import random
from functools import cache
from pathlib import Path
from typing import Literal, Optional
from xmlrpc.client import DateTime

import toml

from leolino_kids_prio.constants import GROUP_SIZE

Kid = str
Group = str
Age = Literal["U3", "Ü3"]


class Data:
    """This classes purpose is to be able to work on different data with the algorithm.

    This is done to test the stuff efficiently.
    """

    def __init__(self, root: Optional[Path] = None):
        self.root = Path(__file__).parent.parent / "data" if root is None else root

    @property
    def allowed_kids_history(self) -> dict[DateTime, list[Kid]]:
        with (self.root / "generated" / "allowed_kids.toml").open("r", encoding="utf-8") as f:
            return toml.load(f)

    @property
    def allowed_groups_history(self) -> dict[DateTime, dict[Age, list[Group]]]:
        with (self.root / "manually_updated" / "allowed_groups.toml").open("r", encoding="utf-8") as f:
            return toml.load(f)

    @property
    def groups(self) -> dict[Age, dict[Group, list[Kid]]]:
        with (self.root / "manually_updated" / "groups.toml").open("r", encoding="utf-8") as f:
            return toml.load(f)

    @property
    def unused_days_history(self) -> list[dict[DateTime, list[Kid]]]:
        with (self.root / "manually_updated" / "unused_days.toml").open("r", encoding="utf-8") as f:
            return toml.load(f)

    @property
    def used_free_spots_history(self) -> list[dict[DateTime, list[Kid]]]:
        with (self.root / "manually_updated" / "used_free_spots.toml").open("r", encoding="utf-8") as f:
            return toml.load(f)

    @property
    def always_allowed_kids(self) -> dict[Age, list[Kid]]:
        with (self.root / "manually_updated" / "always_allowed_kids.toml").open("r", encoding="utf-8") as f:
            return toml.load(f)

    @cache  # noqa: B019
    def tiebreaker(self, prio: int):
        file_path = self.root / "generated" / "tiebreaker" / f"prio_{prio}.txt"
        if not file_path.exists():
            all_kids = list(self.all_kids("U3").union(self.all_kids("Ü3")))
            random.shuffle(all_kids)
            with file_path.open("w", encoding="utf-8") as f:
                f.write("\n".join(all_kids))

        with file_path.open("r") as f2:
            return f2.read().split()

    def all_kids(self, age: Age) -> set[Kid]:
        """Returns the set of all kids in either U3 or Ü3."""
        return set.union(*(set(self.groups[age][group]) for group in self.groups[age]))

    def allowed_and_prio(self, age: Age, groups: list[Group]) -> tuple[list[Kid], int, list[Kid]]:
        """Computes the list of allowed kids (for U3 or Ü3), the number of free spots and a priority list of all other kids.

        Args:
            age:
            groups:

        Returns:
            - allowed_kids: a list of kids that can definitely come, because they are in one of the allowed groups
            - nr_free_spots: the number of free spots which can be filled by the kids in the `prio` list.
            - prio: a list of all other kids sorted by priority (early in the list means higher priority)
        """
        allowed_kids = set.union(*(set(self.groups[age][group]) for group in groups))
        nr_free_spots = len(groups) * GROUP_SIZE[age] - len(allowed_kids)
        other_kids = list(self.all_kids(age) - allowed_kids)
        # other_kids_w_prios = [(kid, self.prio_key(kid)) for kid in other_kids]
        prio = sorted(other_kids, key=lambda kid: self.prio_key(kid))
        return list(allowed_kids), nr_free_spots, prio

    def prio_key(self, kid: Kid) -> tuple[int, int]:
        unused_prio = len([date for date, kids in self.unused_days_history.items() if kid in kids])
        used_prio = len([date for date, kids in self.used_free_spots_history.items() if kid in kids])
        prio = used_prio - unused_prio
        tiebreaker = self.tiebreaker(prio).index(kid)
        assert isinstance(prio, int)
        assert isinstance(tiebreaker, int)
        return prio, tiebreaker
