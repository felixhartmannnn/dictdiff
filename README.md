# dictdiff

Source: https://github.com/felixhartmannnn/dictdiff


<p align="left">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
</p>

Compute minimal, serializable diffs between Python dictionaries.

## About

`dictdiff` compares two Python dictionaries and reports added, removed, and changed keys. It handles nested dictionaries and lists, making it useful for config comparison, migration QA, API payload inspection, and general diff workflows where a structured summary is preferable to raw text diffs.

## Features

- Added, removed, and changed keys with old/new values
- Nested dictionary diffing with dot-separated paths
- List diffing with index-based change reporting
- Length-mismatch handling for lists
- Type-mismatch detection
- JSON CLI for comparing two JSON files
- `--json` flag for machine-readable output
- Typed implementation with no external dependencies

## Installation

```bash
pip install dictdiff
```

## Usage

### Python

```python
from dictdiff import diff

left = {"a": 1, "b": {"c": 2}}
right = {"a": 1, "b": {"c": 3}, "d": 4}

result = diff(left, right)
print(result.added)     # {"d": 4}
print(result.changed)   # {"b.c": {"old": 2, "new": 3}}
print(result.removed)   # {}
print(result.is_empty())  # False
print(result.to_dict())   # {"added": ..., "changed": ..., "removed": ...}
```

### CLI

```bash
dictdiff left.json right.json
dictdiff left.json right.json --json
```

Input files must contain JSON objects.

## Project structure

```
dictdiff.py     - diff engine and CLI
tests/
  test_dictdiff.py
pyproject.toml
README.md
LICENSE
.gitignore
```

## Tags

python, diff, dictionary, json, cli, data
