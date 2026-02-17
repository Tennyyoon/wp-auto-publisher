import json
from pathlib import Path
from typing import Set

STATE_PATH = Path("published_ids.json")

def load_published_ids() -> Set[str]:
    if not STATE_PATH.exists():
        return set()
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return set(data.get("published", []))

def save_published_ids(ids: Set[str]) -> None:
    STATE_PATH.write_text(
        json.dumps({"published": sorted(list(ids))}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
