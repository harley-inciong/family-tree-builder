"""
import_export.py - Serialization, JSON backup, and Sheet/CSV Import and Template generation
"""
import json
import io
import pandas as pd
from typing import Tuple, Optional
from tree_model import FamilyTree, FamilyMember

CSV_COLUMNS = [
    "id",
    "first_name",
    "last_name",
    "nickname",
    "gender",
    "birth_date",
    "death_date",
    "is_living",
    "parent_ids",
    "spouse_ids",
    "notes"
]

def export_tree_to_json(tree: FamilyTree) -> str:
    return json.dumps(tree.to_dict(), indent=2)

def import_tree_from_json(json_str: str) -> FamilyTree:
    data = json.loads(json_str)
    return FamilyTree.from_dict(data)

def generate_csv_template() -> str:
    """Return an example CSV spreadsheet content that users can edit."""
    sample_rows = [
        {
            "id": "1",
            "first_name": "Arthur",
            "last_name": "Pendleton",
            "nickname": "Artie",
            "gender": "M",
            "birth_date": "1932",
            "death_date": "2015",
            "is_living": "FALSE",
            "parent_ids": "",
            "spouse_ids": "2",
            "notes": "Patriarch, clockmaker"
        },
        {
            "id": "2",
            "first_name": "Eleanor",
            "last_name": "Vance",
            "nickname": "Ellie",
            "gender": "F",
            "birth_date": "1936",
            "death_date": "",
            "is_living": "TRUE",
            "parent_ids": "",
            "spouse_ids": "1",
            "notes": "Pianist"
        },
        {
            "id": "3",
            "first_name": "Robert",
            "last_name": "Pendleton",
            "nickname": "Rob",
            "gender": "M",
            "birth_date": "1960",
            "death_date": "",
            "is_living": "TRUE",
            "parent_ids": "1,2",
            "spouse_ids": "",
            "notes": "Civil engineer"
        }
    ]
    df = pd.DataFrame(sample_rows, columns=CSV_COLUMNS)
    return df.to_csv(index=False)

def import_tree_from_sheet(file_bytes: bytes, file_name: str) -> Tuple[Optional[FamilyTree], str]:
    """Parse CSV or XLSX file and construct a FamilyTree."""
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes), dtype=str)
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(file_bytes), dtype=str)
        else:
            return None, "Unsupported file format. Please upload a .csv or .xlsx file."
        
        # Normalize column names (strip, lowercase)
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # Required columns check
        if "first_name" not in df.columns and "name" not in df.columns:
            return None, "Spreadsheet must contain at least a 'first_name' or 'name' column."

        tree = FamilyTree()
        members_map = {}
        row_relations = []

        for idx, row in df.iterrows():
            raw_id = str(row.get("id", "")).strip()
            if not raw_id or raw_id == "nan":
                raw_id = f"mem_imp_{idx + 1}"

            # Name splitting if single 'name' column
            first_name = str(row.get("first_name", "")).strip()
            last_name = str(row.get("last_name", "")).strip()
            if not first_name and "name" in row and str(row.get("name", "")).strip():
                parts = str(row["name"]).strip().split()
                first_name = parts[0] if parts else ""
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

            first_name = "" if first_name == "nan" else first_name
            last_name = "" if last_name == "nan" else last_name
            nickname = str(row.get("nickname", "")).strip()
            nickname = "" if nickname == "nan" else nickname

            gender = str(row.get("gender", "O")).strip().upper()
            if gender.startswith("M") or gender == "MALE":
                gender = "M"
            elif gender.startswith("F") or gender == "FEMALE":
                gender = "F"
            else:
                gender = "O"

            birth_date = str(row.get("birth_date", row.get("birth", ""))).strip()
            birth_date = "" if birth_date == "nan" else birth_date

            death_date = str(row.get("death_date", row.get("death", ""))).strip()
            death_date = "" if death_date == "nan" else death_date

            is_living_raw = str(row.get("is_living", "true")).strip().lower()
            is_living = is_living_raw in ("true", "1", "yes", "t") if not death_date else False

            notes = str(row.get("notes", "")).strip()
            notes = "" if notes == "nan" else notes

            mem = FamilyMember(
                id=raw_id,
                first_name=first_name,
                last_name=last_name,
                nickname=nickname,
                gender=gender,
                birth_date=birth_date,
                death_date=death_date,
                is_living=is_living,
                notes=notes
            )
            tree.add_member(mem)
            members_map[raw_id] = mem

            # Save relations to link after all members exist
            parent_ids_raw = str(row.get("parent_ids", row.get("parent_id", row.get("parents", "")))).strip()
            spouse_ids_raw = str(row.get("spouse_ids", row.get("spouse_id", row.get("spouses", "")))).strip()
            row_relations.append((raw_id, parent_ids_raw, spouse_ids_raw))

        # Now link relationships
        for mem_id, p_raw, s_raw in row_relations:
            if p_raw and p_raw != "nan":
                p_list = [p.strip() for p in p_raw.replace(";", ",").split(",") if p.strip()]
                for pid in p_list:
                    if pid in tree.members:
                        if pid not in tree.members[mem_id].parents:
                            tree.members[mem_id].parents.append(pid)
                        if mem_id not in tree.members[pid].children:
                            tree.members[pid].children.append(mem_id)

            if s_raw and s_raw != "nan":
                s_list = [s.strip() for s in s_raw.replace(";", ",").split(",") if s.strip()]
                for sid in s_list:
                    if sid in tree.members:
                        if sid not in tree.members[mem_id].spouses:
                            tree.members[mem_id].spouses.append(sid)
                        if mem_id not in tree.members[sid].spouses:
                            tree.members[sid].spouses.append(mem_id)

        # Set sensible root
        roots = tree.get_root_candidates()
        if roots:
            tree.root_id = roots[0].id
        elif tree.members:
            tree.root_id = next(iter(tree.members.keys()))

        return tree, f"Successfully imported {len(tree.members)} relatives from spreadsheet!"

    except Exception as e:
        return None, f"Error processing sheet file: {str(e)}"
