import json
from pathlib import Path
import pytest

from tiny_todo.todo import TodoList


def test_add_and_list_open():
    tl = TodoList()
    a = tl.add("write tests")
    b = tl.add("wire CI")
    assert isinstance(a, int) and isinstance(b, int)
    open_items = [t.text for t in tl.list_open()]
    assert open_items == ["write tests", "wire CI"]


def test_complete_and_persistence(tmp_path):
    tl = TodoList()
    a = tl.add("task A")
    b = tl.add("task B")

    # complete one task
    assert tl.complete(a) is True
    assert tl.complete(a) is False  # already completed

    save_path = tmp_path / "todos.json"
    tl.save(save_path)
    assert save_path.exists()

    # reload and check state is preserved
    tl2 = TodoList.load(save_path)
    assert {t.id for t in tl2.list_all()} == {a, b}
    assert {t.text for t in tl2.list_open()} == {"task B"}


def test_add_empty_raises():
    tl = TodoList()
    with pytest.raises(ValueError):
        tl.add("   ")
