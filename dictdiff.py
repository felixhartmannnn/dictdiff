"""dictdiff: Compute minimal, serializable diffs between Python dictionaries."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Union

Value = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]


class DictDiff:
    """Represent the diff between two flat or nested mappings."""

    def __init__(
        self,
        added: Dict[str, Value],
        changed: Dict[str, Dict[str, Value]],
        removed: Dict[str, Value],
    ):
        self.added = added
        self.changed = changed
        self.removed = removed

    def is_empty(self) -> bool:
        return not (self.added or self.changed or self.removed)

    def to_dict(self) -> Dict[str, Any]:
        return {"added": self.added, "changed": self.changed, "removed": self.removed}


def _walk_values(path: str, left: Any, right: Any) -> Dict[str, Dict[str, Value]]:
    diff: Dict[str, Dict[str, Value]] = {}
    if type(left) != type(right):
        diff[path] = {"old": left, "new": right}
        return diff
    if isinstance(left, dict) and isinstance(right, dict):
        diff.update(_diff_dicts(f"{path}." if path else "", left, right))
    elif isinstance(left, list) and isinstance(right, list):
        diff.update(_diff_lists(path, left, right))
    elif left != right:
        diff[path] = {"old": left, "new": right}
    return diff


def _diff_dicts(
    prefix: str,
    left: Dict[str, Any],
    right: Dict[str, Any],
) -> Dict[str, Dict[str, Value]]:
    diff: Dict[str, Dict[str, Value]] = {}
    for key in sorted(set(left) | set(right)):
        path = f"{prefix}{key}"
        if key not in left:
            continue
        if key not in right:
            diff[path] = {"old": left[key], "new": None}
            continue
        diff.update(_walk_values(path, left[key], right[key]))
    return diff


def _diff_lists(
    path: str,
    left: List[Any],
    right: List[Any],
) -> Dict[str, Dict[str, Value]]:
    diff: Dict[str, Dict[str, Value]] = {}
    min_len = min(len(left), len(right))
    for idx in range(min_len):
        item_path = f"{path}[{idx}]"
        diff.update(_walk_values(item_path, left[idx], right[idx]))
    if len(left) > len(right):
        for idx in range(len(right), len(left)):
            diff[f"{path}[{idx}]"] = {"old": left[idx], "new": None}
    elif len(right) > len(left):
        for idx in range(len(left), len(right)):
            diff[f"{path}[{idx}]"] = {"old": None, "new": right[idx]}
    return diff


def diff(left: Dict[str, Value], right: Dict[str, Value]) -> DictDiff:
    added = {key: right[key] for key in right if key not in left}
    removed = {key: left[key] for key in left if key not in right}
    common = {key: left[key] for key in left if key in right}
    changed = _diff_dicts("", common, {k: right[k] for k in common})
    return DictDiff(added=added, changed=changed, removed=removed)


def _print_changed(result: DictDiff) -> None:
    for path, values in result.changed.items():
        print(f"  changed: {path} => {values}")


def _print_diff(result: DictDiff, color: bool) -> None:
    for key, value in result.added.items():
        print(f"  added: {key} => {value}")
    for key, value in result.removed.items():
        print(f"  removed: {key} => {value}")
    _print_changed(result)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Diff two JSON files as dicts.")
    parser.add_argument("left", help="Path to left JSON file")
    parser.add_argument("right", help="Path to right JSON file")
    parser.add_argument("--json", action="store_true", help="Output diff as JSON")
    parser.add_argument("--color", action="store_true", help="Use colorized output")
    args = parser.parse_args(argv)

    def load(path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    try:
        left = load(args.left)
        right = load(args.right)
    except Exception as exc:
        print(f"dictdiff: {exc}", file=sys.stderr)
        return 2

    result = diff(left, right)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, default=str))
    else:
        if result.is_empty():
            print("No differences.")
        else:
            _print_diff(result, args.color)
    return 0 if result.is_empty() else 1


__all__ = ["DictDiff", "Value", "diff", "main"]
