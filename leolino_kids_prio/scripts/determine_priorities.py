from leolino_kids_prio.utils import Data


if __name__ == '__main__':
    age_group = "Ü3"
    allowed_groups = ["B", "C", "D"]

    d = Data()
    allowed, nr, prio = d.allowed_and_prio(age_group, allowed_groups)
    print(f"Today, the groups {allowed_groups} are can come to the daycare. I.e., the kids:")
    print(allowed)
    print("can come.")
    print(f"There are {nr} free spots which can be filled with kids from the priority list, which currently looks like:")
    print(prio)
