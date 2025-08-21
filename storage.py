import json, os, threading, datetime
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

_lock = threading.Lock()

def _path(name: str) -> str:
    return os.path.join(DATA_DIR, name)

def _read(name: str, default):
    p = _path(name)
    if not os.path.exists(p):
        return default
    with _lock, open(p, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return default

def _write(name: str, obj):
    with _lock, open(_path(name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def ensure_data_files():
    for fname, default in [
        ("tasks.json", {"tasks": []}),
        ("habits.json", {"habits": []}),
        ("sessions.json", {"sessions": []}),
        ("reflections.json", {"reflections": []}),
    ]:
        if not os.path.exists(_path(fname)):
            _write(fname, default)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# ---- Tasks ----
def add_tasks(tasks: List[Dict[str, Any]]):
    db = _read("tasks.json", {"tasks": []})
    db["tasks"].extend(tasks)
    _write("tasks.json", db)
    return db["tasks"]

def get_tasks():
    return _read("tasks.json", {"tasks": []})["tasks"]

# ---- Habits ----
def add_habit(name: str):
    db = _read("habits.json", {"habits": []})
    if name and name not in [h["name"] for h in db["habits"]]:
        db["habits"].append({"name": name, "streak": 0, "last_done_date": None})
        _write("habits.json", db)
    return db["habits"]

def toggle_habit(name: str, date_iso: str):
    db = _read("habits.json", {"habits": []})
    for h in db["habits"]:
        if h["name"] == name:
            last = h.get("last_done_date")
            if last != date_iso[:10]:
                if last is None:
                    h["streak"] = 1
                else:
                    last_d = datetime.date.fromisoformat(last)
                    today_d = datetime.date.fromisoformat(date_iso[:10])
                    if (today_d - last_d).days == 1:
                        h["streak"] += 1
                    else:
                        h["streak"] = 1
                h["last_done_date"] = date_iso[:10]
            _write("habits.json", db)
            break
    return db["habits"]

def list_habits():
    return _read("habits.json", {"habits": []})["habits"]

#  Focus sessions 
def add_session(task_text: str, minutes: int, outcome: str):
    db = _read("sessions.json", {"sessions": []})
    db["sessions"].append({
        "ts": now_iso(),
        "task": task_text,
        "minutes": minutes,
        "outcome": outcome
    })
    _write("sessions.json", db)
    return db["sessions"]

def list_sessions():
    return _read("sessions.json", {"sessions": []})["sessions"]

#  Reflections 
def add_reflection(entry: Dict[str, Any]):
    db = _read("reflections.json", {"reflections": []})
    entry["ts"] = now_iso()
    db["reflections"].append(entry)
    _write("reflections.json", db)
    return db["reflections"]

def list_reflections():
    return _read("reflections.json", {"reflections": []})["reflections"]
