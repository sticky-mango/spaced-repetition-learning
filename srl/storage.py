from rich.console import Console
from pathlib import Path
import json

DEFAULT_DIR = Path.home() / ".srl"
CONFIG_FILE = DEFAULT_DIR / "config.json"
DATA_DIR = None
PROGRESS_FILE = None
MASTERED_FILE = None
NEXT_UP_FILE = None
AUDIT_FILE = None


def _ensure_bootstrap_dir():
    DEFAULT_DIR.mkdir(parents=True, exist_ok=True)

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(file_path: Path) -> dict:
    if not file_path.exists():
        return {}
    with open(file_path, "r") as f:
        return json.load(f)


def save_json(file_path: Path, data: dict):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def set_data_dir(console: Console):
    global DATA_DIR
    config = load_json(CONFIG_FILE)
    if config == {}:
        while("data_directory" not in config):
            console.print(f"Enter the data directory path (leave empty for default {DEFAULT_DIR}):")
            path = input().strip()

            console.print(f"chosen path: {path}")
        
            if path:
                data_dir = Path(path).expanduser()
                if not data_dir.is_absolute():
                    console.print("please enter an absolute path")
                elif not data_dir.parent.exists():
                    console.print(f"There is no folder: {data_dir.parent}")
                else:
                    config["data_directory"] = path
                    console.print(config["data_directory"])
            else:   
                config["data_directory"] = str(DEFAULT_DIR)
            
    DATA_DIR = Path(config["data_directory"])
    _ensure_bootstrap_dir()
    ensure_data_dir()
    _init_file_globals(console)

    save_json(CONFIG_FILE, config)


def _init_file_globals(console: Console):
    global PROGRESS_FILE
    global MASTERED_FILE
    global NEXT_UP_FILE
    global AUDIT_FILE
    global CONFIG_FILE

    PROGRESS_FILE = DATA_DIR / "problems_in_progress.json"
    MASTERED_FILE = DATA_DIR / "problems_mastered.json"
    NEXT_UP_FILE = DATA_DIR / "next_up.json"
    AUDIT_FILE = DATA_DIR / "audit.json"
