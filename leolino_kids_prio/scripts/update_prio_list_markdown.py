from leolino_kids_prio.utils import Data

if __name__ == '__main__':
    """run this script to update the files `Prioliste U3.md` and `Prioliste Ü3.md`.
    
    Those files give an overview over the current prio list.
    """
    d = Data()
    d.write_future_prio_list_to_markdown()

