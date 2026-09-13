"""
tree_model.py - Core Genealogical Data Model and Family Tree Graph Operations
"""
import uuid
from typing import Dict, List, Optional, Any

class FamilyMember:
    def __init__(
        self,
        id: Optional[str] = None,
        first_name: str = "",
        last_name: str = "",
        nickname: str = "",
        gender: str = "M",  # 'M' (Male), 'F' (Female), 'O' (Other / Unknown)
        birth_date: str = "",
        death_date: str = "",
        is_living: bool = True,
        notes: str = "",
        is_collapsed: bool = False,
        parents: Optional[List[str]] = None,
        spouses: Optional[List[str]] = None,
        children: Optional[List[str]] = None,
    ):
        self.id = id if id else f"mem_{uuid.uuid4().hex[:8]}"
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.nickname = nickname.strip()
        self.gender = gender if gender in ('M', 'F', 'O') else 'O'
        self.birth_date = birth_date.strip()
        self.death_date = death_date.strip()
        self.is_living = is_living if not death_date.strip() else False
        self.notes = notes.strip()
        self.is_collapsed = is_collapsed
        self.parents = parents or []
        self.spouses = spouses or []
        self.children = children or []

    @property
    def display_name(self) -> str:
        name_parts = []
        if self.first_name:
            name_parts.append(self.first_name)
        if self.nickname:
            name_parts.append(f'"{self.nickname}"')
        if self.last_name:
            name_parts.append(self.last_name)
        return " ".join(name_parts) if name_parts else "Unnamed Member"

    @property
    def lifespan_str(self) -> str:
        b = self.birth_date or "?"
        if self.is_living:
            return f"b. {b}" if self.birth_date else "Living"
        d = self.death_date or "?"
        return f"{b} - †{d}"

    @property
    def symbol_glyph(self) -> str:
        """Universal Genealogical Notation Symbol"""
        if self.gender == 'M':
            return '♂'  # Square / Male
        elif self.gender == 'F':
            return '♀'  # Circle / Female
        else:
            return '◇'  # Diamond / Other / Unknown

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "is_living": self.is_living,
            "notes": self.notes,
            "is_collapsed": self.is_collapsed,
            "parents": list(self.parents),
            "spouses": list(self.spouses),
            "children": list(self.children),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FamilyMember':
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            nickname=data.get("nickname", ""),
            gender=data.get("gender", "O"),
            birth_date=data.get("birth_date", ""),
            death_date=data.get("death_date", ""),
            is_living=data.get("is_living", True),
            notes=data.get("notes", ""),
            is_collapsed=data.get("is_collapsed", False),
            parents=data.get("parents", []),
            spouses=data.get("spouses", []),
            children=data.get("children", []),
        )


class FamilyTree:
    def __init__(self, root_id: Optional[str] = None):
        self.members: Dict[str, FamilyMember] = {}
        self.root_id = root_id

    def add_member(self, member: FamilyMember) -> str:
        self.members[member.id] = member
        if not self.root_id:
            self.root_id = member.id
        return member.id

    def get_member(self, member_id: Optional[str]) -> Optional[FamilyMember]:
        if not member_id:
            return None
        return self.members.get(member_id)

    def update_member(self, member_id: str, **kwargs) -> bool:
        member = self.get_member(member_id)
        if not member:
            return False
        for key, val in kwargs.items():
            if hasattr(member, key):
                setattr(member, key, val)
        if member.death_date and member.death_date.strip():
            member.is_living = False
        return True

    def add_child(self, parent_id: str, child_member: FamilyMember, other_parent_id: Optional[str] = None) -> str:
        parent = self.get_member(parent_id)
        if not parent:
            raise ValueError("Parent member does not exist.")
        
        # Add parent to child's parents
        if parent_id not in child_member.parents:
            child_member.parents.append(parent_id)
            
        if other_parent_id and other_parent_id in self.members:
            if other_parent_id not in child_member.parents:
                child_member.parents.append(other_parent_id)
            if child_member.id not in self.members[other_parent_id].children:
                self.members[other_parent_id].children.append(child_member.id)
                
        self.add_member(child_member)
        if child_member.id not in parent.children:
            parent.children.append(child_member.id)
            
        return child_member.id

    def add_parent(self, child_id: str, parent_member: FamilyMember) -> str:
        child = self.get_member(child_id)
        if not child:
            raise ValueError("Child member does not exist.")
        self.add_member(parent_member)
        if parent_member.id not in child.parents:
            child.parents.append(parent_member.id)
        if child_id not in parent_member.children:
            parent_member.children.append(child_id)
            
        return parent_member.id

    def add_spouse(self, member_id: str, spouse_member: FamilyMember) -> str:
        member = self.get_member(member_id)
        if not member:
            raise ValueError("Member does not exist.")
        self.add_member(spouse_member)
        if spouse_member.id not in member.spouses:
            member.spouses.append(spouse_member.id)
        if member_id not in spouse_member.spouses:
            spouse_member.spouses.append(member_id)
        return spouse_member.id

    def delete_member(self, member_id: str) -> bool:
        if member_id not in self.members:
            return False
        
        # Unlink from others
        for m in self.members.values():
            if member_id in m.children:
                m.children.remove(member_id)
            if member_id in m.parents:
                m.parents.remove(member_id)
            if member_id in m.spouses:
                m.spouses.remove(member_id)
                
        del self.members[member_id]
        
        # Reassign root if deleted was root
        if self.root_id == member_id:
            candidates = self.get_root_candidates()
            self.root_id = candidates[0].id if candidates else (next(iter(self.members.keys())) if self.members else None)
            
        return True

    def get_root_candidates(self) -> List[FamilyMember]:
        """Members who have no registered parents in the tree."""
        return [m for m in self.members.values() if len(m.parents) == 0]

    def count_descendants(self, member_id: str, visited: Optional[set] = None) -> int:
        if visited is None:
            visited = set()
        member = self.get_member(member_id)
        if not member or member_id in visited:
            return 0
        visited.add(member_id)
        count = 0
        for ch_id in member.children:
            if ch_id not in visited:
                count += 1 + self.count_descendants(ch_id, visited)
        return count

    def get_all_descendant_ids(self, member_id: str) -> set:
        visited = set()
        def _collect(mid):
            m = self.get_member(mid)
            if not m:
                return
            for ch in m.children:
                if ch not in visited:
                    visited.add(ch)
                    _collect(ch)
        _collect(member_id)
        return visited

    def search(self, query: str) -> List[FamilyMember]:
        q = query.lower().strip()
        if not q:
            return list(self.members.values())
        results = []
        for m in self.members.values():
            haystack = f"{m.first_name} {m.nickname} {m.last_name} {m.notes} {m.birth_date} {m.death_date}".lower()
            if q in haystack:
                results.append(m)
        return results

    def get_generations_map(self) -> Dict[str, int]:
        """Compute generational levels accurately considering direct descent and spouse alignment."""
        gen_map: Dict[str, int] = {}
        if not self.members:
            return gen_map

        # Helper to compute generation from known parents
        def compute_depth(mid: str, visited: set) -> int:
            if mid in visited:
                return 1
            visited.add(mid)
            m = self.get_member(mid)
            if not m or not m.parents:
                return 1
            parent_gens = [compute_depth(p, visited.copy()) for p in m.parents if self.get_member(p)]
            return max(parent_gens, default=0) + 1

        # Iteratively settle generational levels
        changed = True
        iterations = 0
        while changed and iterations < 15:
            changed = False
            iterations += 1
            for mid, m in self.members.items():
                old_val = gen_map.get(mid)
                new_val = compute_depth(mid, set())
                
                # Check if spouse has a higher generation to align couples
                for sp_id in m.spouses:
                    sp_gen = gen_map.get(sp_id, 1)
                    if sp_gen > new_val:
                        new_val = sp_gen

                # Also if this member is parent of someone, ensure generation is at least child - 1
                for ch_id in m.children:
                    ch_gen = gen_map.get(ch_id)
                    if ch_gen and new_val < ch_gen:
                        # parent must be strictly above child or at least consistent
                        pass

                if old_val != new_val:
                    gen_map[mid] = new_val
                    changed = True

        for mid in self.members:
            if mid not in gen_map:
                gen_map[mid] = 1

        return gen_map

    def get_generation_depth(self) -> int:
        gen_map = self.get_generations_map()
        return max(gen_map.values(), default=0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "root_id": self.root_id,
            "members": {mid: m.to_dict() for mid, m in self.members.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FamilyTree':
        tree = cls(root_id=data.get("root_id"))
        for mid, m_data in data.get("members", {}).items():
            tree.add_member(FamilyMember.from_dict(m_data))
        tree.root_id = data.get("root_id")
        if not tree.root_id and tree.members:
            tree.root_id = next(iter(tree.members.keys()))
        return tree
