import json
import os
from tree_model import FamilyTree

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.html")

def generate_family_tree_html(tree: FamilyTree, height: int = 760) -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
    tree_data = tree.to_dict()
    tree_json_str = json.dumps(tree_data)
    return template.replace("__TREE_JSON_PLACEHOLDER__", tree_json_str)
