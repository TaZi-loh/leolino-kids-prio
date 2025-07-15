import random
from copy import deepcopy
from functools import cache
from pathlib import Path
from typing import Literal, Optional
from xmlrpc.client import DateTime

import toml
from multiset import Multiset

from leolino_kids_prio.constants import GROUP_SIZE

Kid = str
Group = str  # A, B, C, ...
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

    @property
    def starting_prio(self) -> dict[Age, dict[Kid, int]]:
        file_path = self.root / "generated" / "starting_prio.toml"
        if not file_path.exists():
            with file_path.open("w", encoding="utf-8") as f:
                toml.dump({"U3": {}, "Ü3": {}}, f)
        with (self.root / "generated" / "starting_prio.toml").open("r", encoding="utf-8") as f:
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
            return f2.read().split("\n")

    def all_kids(self, age: Age) -> set[Kid]:
        """Returns the set of all kids in either U3 or Ü3."""
        return set.union(*(set(self.groups[age][group]) for group in self.groups[age]))

    def allowed_and_prio(self, age: Age, groups: list[Group]) -> tuple[list[Kid], int, list[Kid], Multiset[Kid]]:
        """Computes the list of allowed kids (for U3 or Ü3), the number of free spots and a priority list of other kids.

        Args:
            age:
            groups:

        Returns:
            - allowed_kids: a list of kids that can definitely come, because they are in one of the allowed groups
            - nr_free_spots: the number of free spots which can be filled by the kids in the `prio` list.
            - prio: a list of all other kids sorted by priority (early in the list means higher priority)
            - duplicates: multiset of kids that were duplicated because they appear in more than one group.
        """
        allowed_kids_with_duplicates = Multiset.combine(*(Multiset(self.groups[age][group]) for group in groups)) if len(groups) > 0 else Multiset()
        allowed_kids_no_duplicates = set(allowed_kids_with_duplicates)
        duplicates = allowed_kids_with_duplicates.difference(allowed_kids_no_duplicates)
        nr_free_spots = len(groups) * GROUP_SIZE[age] - len(allowed_kids_no_duplicates)
        other_kids = list(self.all_kids(age) - allowed_kids_no_duplicates)
        # other_kids_w_prios = [(kid, self.prio_key(kid)) for kid in other_kids]
        prio = sorted(other_kids, key=lambda kid: self.prio_key(kid))
        return list(allowed_kids_no_duplicates), nr_free_spots, prio, duplicates

    @staticmethod
    def fill_up(prio: list[Kid], nr_free_spots: int, duplicates: Multiset[Kid], stay_home_kids: list[Kid]) -> tuple[list[tuple[Kid, Optional[Kid], str]], list[Kid]]:
        """

        Args:
            age: the age group that is concerned
            prio: the calculated priority list
            nr_free_spots: the number of free spots which can be filled by the kids in the `prio` list.
            duplicates: multiset of kids that were duplicated because they appear in more than one group.
            stay_home_kids: a list of kids that will stay home on this day.

        Returns:
            - A list of triple of (kid, kid, comment). The first kid will take the spot of the second kid.
              The comment describes special cases
            - A list of kids that stay home and would offer their spot, but there is no one to use that spot.
        """
        prio = deepcopy(prio)
        duplicates = deepcopy(duplicates)
        stay_home_kids = deepcopy(stay_home_kids)
        result = []
        while len(prio) > 0 and len(duplicates) > 0:
            kid_highest_prio = prio.pop(0)
            if kid_highest_prio not in stay_home_kids:
                kid_duplicate = next(iter(duplicates))
                result.append((kid_highest_prio, kid_duplicate, f"s {duplicates.remove(kid_duplicate, 1) + 1}. Platz"))
                nr_free_spots -= 1
            else:
                stay_home_kids = [kid for kid in stay_home_kids if kid != kid_highest_prio]
        while len(prio) > 0 and nr_free_spots > 0:
            kid_highest_prio = prio.pop(0)
            if kid_highest_prio not in stay_home_kids:
                result.append((kid_highest_prio, None, f"freier Platz in einer der Gruppen"))
                nr_free_spots -= 1
            else:
                stay_home_kids = [kid for kid in stay_home_kids if kid != kid_highest_prio]
        while len(prio) > 0 and len(stay_home_kids) > 0:
            kid_highest_prio = prio.pop(0)
            if kid_highest_prio not in stay_home_kids:
                kid_stay_home = stay_home_kids.pop(0)
                result.append((kid_highest_prio, kid_stay_home, ""))
            else:
                stay_home_kids = [kid for kid in stay_home_kids if kid != kid_highest_prio]
        return result, stay_home_kids

    def full_announcement_and_toml_update(self, date: str, u3_groups: list[Group], u3_stay_home_kids: list[Kid], ue3_groups: list[Group], ue3_stay_home_kids: list[Kid]) -> str:
        ann_u3, fill_ups_u3, leftover_stay_home_kids_u3 = self.announcement_age_group(date, "U3", u3_groups, u3_stay_home_kids)
        ann_ue3, fill_ups_ue3, leftover_stay_home_kids_ue3 = self.announcement_age_group(date, "Ü3", ue3_groups, ue3_stay_home_kids)
        announcement = f"{ann_u3}\n\n\n\n{ann_ue3}"
        print(announcement)

        used_free_spots = self.used_free_spots_history
        used_free_spots[date] = [fu[0] for fu in fill_ups_u3 + fill_ups_ue3]
        with (self.root / "manually_updated" / "used_free_spots.toml").open("w", encoding="utf-8") as f:
            toml.dump(used_free_spots, f)

        unused_days = self.unused_days_history
        unused_days[date] = [fu[1] for fu in fill_ups_u3 + fill_ups_ue3 if fu[1] is not None and fu[2] == ""] + leftover_stay_home_kids_u3 + leftover_stay_home_kids_ue3
        with (self.root / "manually_updated" / "unused_days.toml").open("w", encoding="utf-8") as f:
            toml.dump(unused_days, f)

        allowed_groups = self.allowed_groups_history
        allowed_groups[date] = {}
        allowed_groups[date]["U3"] = u3_groups
        allowed_groups[date]["Ü3"] = ue3_groups
        with (self.root / "manually_updated" / "allowed_groups.toml").open("w", encoding="utf-8") as f:
            toml.dump(allowed_groups, f)

        return announcement

    def announcement_age_group(self, date: str, age: Age, groups: list[Group], stay_home_kids: list[Kid]) -> tuple[str, list[tuple[Kid, Optional[Kid], str]], list[Kid]]:
        allowed_kids, nr_free_spots, prio, duplicates = self.allowed_and_prio(age, groups)
        fill_ups, leftover_stay_home_kids = self.fill_up(prio, nr_free_spots, duplicates, stay_home_kids)
        fill_ups_ = [f"{fu[0]} ({"" if fu[1] is None else fu[1]}{fu[2]})" for fu in fill_ups]

        result = f"Am {date} dürfen die {age} Gruppen {groups} in die Kita kommen. Das heißt, die folgenden Kinder dürfen kommen:\n"
        result += f"{allowed_kids}\n\n"
        result += f"Es gibt {nr_free_spots} freie Plätze, die mit Kindern von der Prioritätenliste gefüllt werden können. Diese sieht aktuell so aus:\n"
        result += f"{prio}\n\n"
        result += "Außerdem werden folgende Kinder nicht kommen:\n"
        result += f"{stay_home_kids}\n\n"
        result += "Daraus ergibt sich, dass die folgenden Kinder kommen dürfen und den Platz des jeweils in Klammern genannten Kindes einnehmen:\n"
        result += "\n".join(fill_ups_)
        return result, fill_ups, leftover_stay_home_kids

    def prio_key(self, kid: Kid) -> tuple[int, int]:
        unused_prio = len([date for date, kids in self.unused_days_history.items() if kid in kids])
        used_prio = len([date for date, kids in self.used_free_spots_history.items() if kid in kids])
        starting_prio_u3 = self.starting_prio["U3"].get(kid)
        starting_prio_ue3 = self.starting_prio["Ü3"].get(kid)
        assert starting_prio_u3 is None or starting_prio_ue3 is None, "duplicated kid name."
        if starting_prio_u3 is not None:
            starting_prio = starting_prio_u3
        elif starting_prio_ue3 is not None:
            starting_prio = starting_prio_ue3
        else:
            starting_prio = 0  # these are the kids from the beginning, which we did not list explicitely
        prio = used_prio - unused_prio + starting_prio
        tiebreaker = self.tiebreaker(prio).index(kid)
        assert isinstance(prio, int)
        assert isinstance(tiebreaker, int)
        return prio, tiebreaker


def all_kids(u3_groups: dict[Group, list[Kid]], ue3_groups: dict[Group, list[Kid]]) -> set[Kid]:
    """Returns the set of all kids in all groups."""
    result = set()
    for kids in u3_groups.values():
        for kid in kids:
            result.add(kid)
    for kids in ue3_groups.values():
        for kid in kids:
            result.add(kid)
    return result


def insert_random_line(filename: str | Path, new_line: str) -> None:
    # Read the file into a list of lines
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Generate a random index
    index = random.randint(0, len(lines))  # include end of file as a valid position

    # Insert the new line (make sure it ends with a newline character)
    lines.insert(index, new_line if new_line.endswith('\n') else new_line + '\n')

    # Write the lines back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)