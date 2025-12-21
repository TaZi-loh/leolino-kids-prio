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
        date="15.12.2025",
        # u3_allowed_groups=["1", "2", "3", "4"],
        u3_allowed_groups=["1", "4"],
        u3_stay_home_kids=["Yuna", "Khan", "Marissa", "Yian"],  # weg: Adya bis 16.1., Aris 22.12.-23.12,
        # ue3_allowed_groups=["A", "B", "C", "D"],
        ue3_allowed_groups=["A", "B", "C", "D"],
        ue3_stay_home_kids=[]  #  weg: Lea 14.1.-16.1.26, 22.12-06.01 Lian, 24.12.25-22.01.26 Sophia G, 22.12-09.01 Holly
    )
    print(full_ann)
    print("\n\nupdating future prio list...")
    d.write_future_prio_list_to_markdown()

