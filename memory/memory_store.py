import json
import os
import threading
from typing import List, Dict, Any


class TaskMemory:
    """
    Simple file-based long term memory for tasks.
    Stored in memory_bank.json so it persists between runs.
    """

    def __init__(self, path: str = "memory/memory_bank.json"):
        self.path = path
        self.lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"tasks": []}, f, ensure_ascii=False, indent=2)

    def _read(self) -> Dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_task(self, task: str) -> None:
        with self.lock:
            data = self._read()
            if task not in data.get("tasks", []):
                data.setdefault("tasks", []).append(task)
                self._write(data)

    def get_tasks(self) -> List[str]:
        if not os.path.exists(self.path):
            return []
        return self._read().get("tasks", [])
