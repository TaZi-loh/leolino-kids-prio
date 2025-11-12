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


def add_kid(kid: Kid, age: Age, always_allowed: bool, starting_prio: int | None = None) -> None:
    d = Data()
    for file in (d.root / "generated" / "tiebreaker").glob("prio_*.txt"):
        insert_random_line(file, kid)
    if always_allowed:
        aak = d.always_allowed_kids
        aak[age].append(kid)
        with (d.root / "manually_updated" / "always_allowed_kids.toml").open("w", encoding="utf-8") as f:
            toml.dump(aak, f)

    # define starting prios
    if starting_prio is None:
        _, _, current_prio_list, _ = d.allowed_and_prio(age, [])
        prio_values = [d.prio_key(kid) for kid in current_prio_list]
        starting_prio = prio_values[len(prio_values) // 2][0]  # the median prio

    starting_prio_dict = d.starting_prio
    assert kid not in starting_prio_dict[age]
    starting_prio_dict[age][kid] = starting_prio
    with (d.root / "generated" / "starting_prio.toml").open("w", encoding="utf-8") as f2:
        toml.dump(starting_prio_dict, f2)


if __name__ == '__main__':
    """
    To add or remove kids, adjust this script and afterward, run `define_new_groups()`.
    """
    remove_kids([])
    # first we need to make sure, that all prio files that need to exist,
    print("we will now give some new kids some tiebreakers and a starting priority.")
    for age in ["U3", "Ü3"]:
        Data().allowed_and_prio(age, [])  # this queries the prio of everybody.
    for kid in ["Yian", "Yuna", ]:
        add_kid(kid, age="U3", always_allowed=False, starting_prio=None)
    for kid in ["Hagen", "Aurelian", "Sophia G.", "Louise", "Sami", ]:
        add_kid(kid, age="Ü3", always_allowed=False, starting_prio=None)
    print("make sure, to run `define_new_groups()` too, to also add the kids to some new group.")



