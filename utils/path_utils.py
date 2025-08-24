from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def get_database_path() -> Path:
    db_path = get_project_root() / "database" / "db.json"
    db_path.parent.mkdir(exist_ok=True)
    return db_path