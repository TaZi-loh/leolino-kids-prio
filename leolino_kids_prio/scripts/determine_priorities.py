from leolino_kids_prio.utils import Data


if __name__ == '__main__':
    """run this script to create the announcement.
    
    Some .toml files are modified by this script. The current implementation also considers used and unused
    spots from the future. Hence, running this script twice will yield a different announcement.
    If you want to avoid this, 
    
    run the script in debug mode up to the printing of the announcement.
    """
    d = Data()
    full_ann = d.full_announcement_and_toml_update(
        date="28.01.2026",
        # u3_allowed_groups=["1", "2", "3", "4"],
        u3_allowed_groups=["3", "4"],
        u3_stay_home_kids=["Yian", "Yuna", "Aris", "Mattis"],
        # ue3_allowed_groups=["A", "B", "C", "D"],
        ue3_allowed_groups=["A", "B", "C", "D"],
        ue3_stay_home_kids=[],
    )
    print(full_ann)
    print("\n\nupdating future prio list...")
    d.write_future_prio_list_to_markdown()

