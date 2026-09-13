"""
sample_data.py - Pre-populated Genealogical Sample Dataset for instant exploration
"""
from tree_model import FamilyTree, FamilyMember

def get_sample_family_tree() -> FamilyTree:
    tree = FamilyTree()

    # Generation 1 (Grandparents)
    arthur = FamilyMember(
        id="mem_arthur_1",
        first_name="Arthur",
        last_name="Pendleton",
        nickname="Artie",
        gender="M",
        birth_date="1932",
        death_date="2015",
        is_living=False,
        notes="Patriarch, clockmaker and botanist."
    )
    eleanor = FamilyMember(
        id="mem_eleanor_1",
        first_name="Eleanor",
        last_name="Vance",
        nickname="Ellie",
        gender="F",
        birth_date="1936",
        death_date="",
        is_living=True,
        notes="Pianist and family archivist."
    )
    arthur.spouses = [eleanor.id]
    eleanor.spouses = [arthur.id]

    tree.add_member(arthur)
    tree.add_member(eleanor)
    tree.root_id = arthur.id

    # Generation 2 (Children of Arthur & Eleanor)
    robert = FamilyMember(
        id="mem_robert_2",
        first_name="Robert",
        last_name="Pendleton",
        nickname="Rob",
        gender="M",
        birth_date="1960",
        death_date="",
        is_living=True,
        notes="Civil engineer. Preserves family homestead."
    )
    sarah = FamilyMember(
        id="mem_sarah_2",
        first_name="Sarah",
        last_name="Montgomery",
        nickname="Sally",
        gender="F",
        birth_date="1963",
        death_date="",
        is_living=True,
        notes="Architect and landscape designer."
    )
    robert.spouses = [sarah.id]
    sarah.spouses = [robert.id]

    tree.add_child(arthur.id, robert, other_parent_id=eleanor.id)
    tree.add_member(sarah)

    clara = FamilyMember(
        id="mem_clara_2",
        first_name="Clara",
        last_name="Pendleton",
        nickname="Claire",
        gender="F",
        birth_date="1965",
        death_date="2021",
        is_living=False,
        notes="Professor of European Literature."
    )
    tree.add_child(arthur.id, clara, other_parent_id=eleanor.id)

    # Generation 3 (Children of Robert & Sarah)
    lucas = FamilyMember(
        id="mem_lucas_3",
        first_name="Lucas",
        last_name="Pendleton",
        nickname="Luke",
        gender="M",
        birth_date="1992",
        death_date="",
        is_living=True,
        notes="Software developer & family tree enthusiast."
    )
    tree.add_child(robert.id, lucas, other_parent_id=sarah.id)

    maya = FamilyMember(
        id="mem_maya_3",
        first_name="Maya",
        last_name="Pendleton",
        nickname="May",
        gender="F",
        birth_date="1996",
        death_date="",
        is_living=True,
        notes="Pediatrician and avid hiker."
    )
    tree.add_child(robert.id, maya, other_parent_id=sarah.id)

    return tree
