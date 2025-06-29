import toml

from leolino_kids_prio.scripts.add_remove_kid import remove_kids
from leolino_kids_prio.utils import Data, all_kids

if __name__ == '__main__':
    new_u3_groups = {
        "A": ["Lian", "Luca", "Khan", "Leia", "Giulio", "Thomas"],
        "B": ["Ava", "Constantin", "Emma", "Leia", "Leonie"],
        "C": ["Viola", "Robert", "Adya", "Leia", "Emilia"],
        "D": ["Tino", "Lisa", "Marissa", "Leia", "Aaron"],
    }
    new_ue3_groups = {
        "A": ["Benjamin", "Mila", "Sofia", "Chleo", "Sara", "Ana Laura", "Larissa", "Felix", "Zsigmond"],
        "B": ["Conrad", "Ferdinand", "Nela", "Damian", "Kylian", "Valentina", "Lukas", "Valentin"],
        "C": ["Liam", "Hayley Xin", "Mani", "Moritz", "Lea Amelie", "Emin", "Gabriel", "Karlo"],
        "D": ["Jeremyas-Max", "Ananya", "Juna", "Yasmin", "Max", "Camille", "Lars"],
    }

    d = Data()
    all_kids_old = all_kids(d.groups["U3"], d.groups["Ü3"])
    all_kids_new = all_kids(new_u3_groups, new_ue3_groups)
    new_kids = all_kids_new.difference(all_kids_old)
    gone_kids = all_kids_old.difference(all_kids_new)
    print(f"The following kids are removed because they are in no group anymore: {gone_kids}")
    remove_kids(gone_kids)
    print(f"The following kids should be added with the function `add_kid()`: {new_kids}")

    with (d.root / "manually_updated" / "groups.toml").open("w", encoding="utf-8") as f:
        toml.dump({"U3": new_u3_groups, "Ü3": new_ue3_groups}, f)
