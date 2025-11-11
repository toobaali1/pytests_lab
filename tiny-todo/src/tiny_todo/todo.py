from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
import json
from pathlib import Path


@dataclass
class TodoItem:
    id: int
    text: str
    done: bool = False


@dataclass
class TodoList:
    _items: List[TodoItem] = field(default_factory=list)
    _next_id: int = 1

    def add(self, text: str) -> int:
        """Add a new todo and return its id."""
        text = (text or "").strip()
        if not text:
            raise ValueError("Todo text cannot be empty.")
        item = TodoItem(id=self._next_id, text=text, done=False)
        self._items.append(item)
        self._next_id += 1
        return item.id

    def complete(self, todo_id: int) -> bool:
        """Mark a todo as done. Returns True if changed, False if not found or already done."""
        for it in self._items:
            if it.id == todo_id:
                if it.done:
                    return False
                it.done = True
                return True
        return False

    def list_open(self) -> List[TodoItem]:
        return [it for it in self._items if not it.done]

    def list_all(self) -> List[TodoItem]:
        return list(self._items)

    def save(self, path: str | Path) -> None:
        p = Path(path)
        data = {
            "next_id": self._next_id,
            "items": [asdict(i) for i in self._items],
        }
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "TodoList":
        p = Path(path)
        if not p.exists():
            # empty list if file not present
            return cls()
        data = json.loads(p.read_text(encoding="utf-8"))
        items = [TodoItem(**raw) for raw in data.get("items", [])]
        tl = cls(items, data.get("next_id", (max((i.id for i in items), default=0) + 1)))
        return tl
