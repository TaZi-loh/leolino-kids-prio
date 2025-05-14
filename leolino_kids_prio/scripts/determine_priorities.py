from leolino_kids_prio.utils import Data


if __name__ == '__main__':
    d = Data()
    full_ann = d.full_announcement_and_toml_update(
        date="15.05.2025",
        u3_groups=["A", "B"],
        u3_stay_home_kids=["Khan", "Holly", "Viola", "Emilia", "Robert", "Ava"],
        ue3_groups=["A", "C", "D"],
        ue3_stay_home_kids=["Karlo", "Camille", "Damian", "Emin", "Valentin", "Taro", "Moritz", "Jeremyas-Max", "Felix", "Larissa", "Ana Laura"],
    )
    print(full_ann)

