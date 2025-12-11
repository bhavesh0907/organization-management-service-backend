import re

def org_name_to_collection_name(org_name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", org_name).lower().strip("_")
    return f"org_{slug}"

