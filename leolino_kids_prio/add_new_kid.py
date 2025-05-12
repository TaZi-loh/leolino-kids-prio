import argparse
import random
from pathlib import Path

import toml

from leolino_kids_prio.utils import Data


def add_kid_to_group(data_path: Path, age_group: str, group: str, kid: str):
    # Datei laden
    groups_file = data_path / "manually_updated" / "groups.toml"
    with groups_file.open("r", encoding="utf-8") as f:
        groups = toml.load(f)

    # Kind zur Gruppe hinzufügen
    if age_group in groups and group in groups[age_group]:
        if kid not in groups[age_group][group]:
            groups[age_group][group].append(kid)
        else:
            print(f"{kid} ist bereits in der Gruppe {group}, bitte geben Sie zusätzlich den Nachnamen an.")
    else:
        print(f"Gruppe {group} in {age_group} existiert nicht.")
        return

    # Datei speichern
    # with groups_file.open("w", encoding="utf-8") as f:
    #     toml.dump(groups, f)
    # print(f"{kid} wurde erfolgreich zur Gruppe {group} in {age_group} hinzugefügt.")

    # Kind random einsortieren.
    d = Data(data_path)
    _, _, u3_prio_list = d.allowed_and_prio("U3", [])
    random_kid_index = random.randint(0, len(u3_prio_list))  # noqa: S311


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fügt ein Kind zu einer Gruppe in der groups.toml hinzu und wählt einen zufälligen Platz in der Prioliste aus."
    )
    parser.add_argument("altersgruppe", type=str, help="Die Altersgruppe (z.B. 'U3' oder 'Ü3').")
    parser.add_argument("gruppe", type=str, help="Die Gruppe (z.B. 'A', 'B', ...).")
    parser.add_argument("name", type=str, help="Der Name des Kindes, das hinzugefügt werden soll.")
    parser.add_argument("--data", type=Path, default=Path("data"), help="Pfad zur Datenablage (Standard: './data').")

    args = parser.parse_args()
    add_kid_to_group(args.data, args.altersgruppe, args.gruppe, args.name)
