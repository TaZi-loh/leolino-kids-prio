from leolino_kids_prio.utils import Data


if __name__ == '__main__':
    date = "14. Mai 2025"
    age_group = "Ü3"
    allowed_groups = ["A", "B", "C"]

    d = Data()
    allowed, nr, prio = d.allowed_and_prio(age_group, allowed_groups)
    print(f"Am {date} dürfen die Gruppen {allowed_groups} in die Kita kommen. Das heißt, die folgenden Kinder dürfen kommen:")
    print(allowed)
    print("can come.")
    print(f"Es gibt {nr} freie Plätze, die mit Kindern von der Prioritätenliste gefüllt werden können. Diese sieht aktuell so aus:")
    print(prio)
    print("\n\n\n")
    print(f"Tomorrow, the groups {allowed_groups} can come to the daycare. I.e., the kids:")
    print(allowed)
    print("can come.")
    print(f"There are {nr} free spots which can be filled with kids from the priority list, which currently looks like:")
    print(prio)
