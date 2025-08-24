import json
from pathlib import Path
from utils.path_utils import get_database_path

def get_db() -> dict:
    db_path = get_database_path()
    
    if db_path.exists():
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("db.json повреждён")
            return {}
    else:
        print("db.json не найден")
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
        return {}

def save_db(data: dict) -> None:
    with open(get_database_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)