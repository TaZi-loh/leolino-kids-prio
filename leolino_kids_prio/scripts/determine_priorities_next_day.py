from leolino_kids_prio.utils import Data


if __name__ == '__main__':
    """run this script to create the announcement.
    
    Some .toml files are modified by this script. The current implementation also considers used and unused
    spots from the future. Hence, running this script twice will yield a different announcement.
    If you want to avoid this, 
    
    run the script in debug mode up to the printing of the announcement.
    """
    d = Data()
    full_ann = d.full_announcement_and_toml_update(date="19.05.2025", u3_allowed_groups=["B", "C"],
                                                   u3_stay_home_kids=[], ue3_allowed_groups=["A", "B", "C", "D"],
                                                   ue3_stay_home_kids=[])
    print(full_ann)

