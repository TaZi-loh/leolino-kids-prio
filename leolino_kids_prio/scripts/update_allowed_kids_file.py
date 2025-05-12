import toml

from leolino_kids_prio.utils import Data

if __name__ == '__main__':
    data = Data()
    new_entries = {}
    for date, age2groups in data.allowed_groups_history.items():
        if date not in data.allowed_kids_history:
            kids_list = []
            for age in ("U3", "Ü3"):
                if age in age2groups:
                    # add all kids from the listed groups to the allowed kids history
                    for group in age2groups[age]:
                        kids_list.extend(data.groups[age][group])
                else:
                    # add all kids from all groups to the allowed kids history
                    for group in data.groups[age]:
                        kids_list.extend(data.groups[age][group])
            kids_list = list(sorted(set(kids_list)))
            new_entries[date] = kids_list
    all_entries = data.allowed_kids_history
    all_entries.update(new_entries)
    with (data.root / "generated" / "allowed_kids.toml").open("w", encoding="utf-8") as f:
        toml.dump(all_entries, f)
