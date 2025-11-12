import toml

from leolino_kids_prio.scripts.add_remove_kid import remove_kids
from leolino_kids_prio.utils import Data, all_kids

if __name__ == '__main__':
    """This should be ran after `add_remove_kids()` was run."""
    new_u3_groups = {
        "1": ["Yian", "Yuna", "Giulio", ],
        "2": ["Ava", "Constantin", "Adam", "Cloe", "Mattis"],
        "3": ["Viola", "Robert", "Adya", "Leia"],
        "4": ["Tino", "Lisa", "Marissa", "Aaron", "Adam"],
    }
    new_ue3_groups = {
        "A": [ "Sofia", "Sara", "Felix", "Jakob", "Sunny", "Noah", "Lennart", "Emma", "Hagen", "Aurelian", "Hayley Xin", ],
        "B": [ "Conrad", "Nela", "Damian", "Kylian", "Valentina", "Lukas", "Mai An", "Holly", "Thomas", "Luca", "Khan", ],
        "C": [ "Liam", "Sophia G.", "Moritz", "Lea Amelie", "Gabriel", "Karlo", "Taro", "Maximilian", "Lian", ],
        "D": [ "Leo", "Jeremyas-Max", "Ananya", "Juna", "Yasmin", "Max", "Lars", "Emilia", "Louise", "Sami"],
    }

    d = Data()
    all_kids_old = all_kids(d.groups["U3"], d.groups["Ü3"])
    all_kids_new = all_kids(new_u3_groups, new_ue3_groups)
    new_kids = all_kids_new.difference(all_kids_old)
    gone_kids = all_kids_old.difference(all_kids_new)
    print(f"The following kids are removed because they are in no group anymore: {gone_kids}")
    remove_kids(gone_kids)
    new_kids_to_add = []
    for new_kid in new_kids:
        for file in (d.root / "generated" / "tiebreaker").glob("*.txt"):
            with file.open("r") as f:
                if new_kid not in f.read().split("\n"):
                    new_kids_to_add.append(new_kid)
    if len(new_kids_to_add) > 0:
        raise ValueError(f"The following kids should be added with the function `add_kid()` first: {new_kids_to_add}")

    with (d.root / "manually_updated" / "groups.toml").open("w", encoding="utf-8") as f:
        toml.dump({"U3": new_u3_groups, "Ü3": new_ue3_groups}, f)
