import toml

from leolino_kids_prio.scripts.add_remove_kid import remove_kids
from leolino_kids_prio.utils import Data, all_kids

if __name__ == '__main__':
    new_u3_groups = {
        "A": ["Lian", "Luca", "Khan", "Leia"],
        "B": ["Ava", "Thomas", "Emma", "Leia"],
        "C": ["Viola", "Aaron", "Adya", "Leia"],
        "D": ["Tino", "Lisa", "Marissa", "Leia"],
        "E": ["Emilia", "Robert", "Constantin", "Leia"],
        "F": ["Giulio", "Caiyi", "Leia"],
        "G": ["Leonie", "Leia", "Holly"],
    }
    new_ue3_groups = {
        "A": ["Noah", "Sunny", "Leo", "Sofia", "Chleo", "Jeremyas-Max", "Ana Laura", "Larissa", "Felix", "Holly",],
        "B": ["Conrad", "Ferdinand", "Ananya", "Damian", "Kylian", "Lukas", "Noah", "Valentina", "Nela", "Holly",],
        "C": ["Noah", "Yasmin", "Hayley Xin", "Max", "Camille", "Lars", "Emin", "Gabriel", "Karlo", "Valentin", "Holly",],
        "D": ["Sara", "Juna", "Yuan", "Liam", "Noah", "Mani", "Moritz", "Lea Amelie", "Jakob", "Taro", "Holly",],
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
