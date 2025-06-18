from typing import Iterable

import toml

from leolino_kids_prio.utils import Data, Kid, Age, insert_random_line


def remove_kids(kids: Iterable[Kid]):
    for remove_kid in kids:
        d = Data()
        for file in (d.root / "generated" / "tiebreaker").glob("prio_*.txt"):
            with file.open("r") as f:
                tiebreaker_kids = f.read().splitlines()
            tiebreaker_kids = [kid for kid in tiebreaker_kids if kid != remove_kid]
            with file.open("w") as f2:
                f2.write("\n".join(tiebreaker_kids))

        aak = d.always_allowed_kids
        for age in aak:
            aak[age] = [kid for kid in aak[age] if kid != remove_kid]
        with (d.root / "manually_updated" / "always_allowed_kids.toml").open("w", encoding="utf-8") as f3:
            toml.dump(aak, f3)

        groups = d.groups
        for age in groups:
            age_group = groups[age]
            for group_name in age_group:
                age_group[group_name] = [kid for kid in age_group[group_name] if kid != remove_kid]
        with (d.root / "manually_updated" / "groups.toml").open("w", encoding="utf-8") as f4:
            toml.dump(groups, f4)


def add_kid(kid: Kid, age: Age, always_allowed: bool) -> None:
    d = Data()
    for file in (d.root / "generated" / "tiebreaker").glob("prio_*.txt"):
        insert_random_line(file, kid)
    if always_allowed:
        aak = d.always_allowed_kids
        aak[age].append(kid)
        with (d.root / "manually_updated" / "always_allowed_kids.toml").open("w", encoding="utf-8") as f:
            toml.dump(aak, f)
    # todo introduce initial prio and set it to the median prio of the age group for a new kid


if __name__ == '__main__':
    """this script should be executed, if a kid leaves the daycare and should not be listed anywhere anymore."""
    # remove_kids(["Timo", "Tina"])
