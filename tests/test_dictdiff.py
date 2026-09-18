from __future__ import annotations

from dictdiff import diff


def test_diff_added():
    left = {"a": 1}
    right = {"a": 1, "b": 2}
    result = diff(left, right)
    assert result.added == {"b": 2}
    assert result.removed == {}
    assert result.changed == {}
    assert result.is_empty() is False


def test_diff_removed():
    left = {"a": 1, "b": 2}
    right = {"b": 2}
    result = diff(left, right)
    assert result.added == {}
    assert result.removed == {"a": 1}
    assert result.changed == {}
    assert result.is_empty() is False


def test_diff_changed():
    left = {"a": 1}
    right = {"a": 2}
    result = diff(left, right)
    assert result.changed == {"a": {"old": 1, "new": 2}}
    assert result.added == {}
    assert result.removed == {}
    assert result.is_empty() is False


def test_diff_empty():
    left = {"a": 1}
    right = {"a": 1}
    result = diff(left, right)
    assert result.is_empty() is True


def test_diff_nested():
    left = {"a": {"b": 1}}
    right = {"a": {"b": 2}}
    result = diff(left, right)
    assert result.changed == {"a.b": {"old": 1, "new": 2}}
    assert result.is_empty() is False


def test_diff_list_items():
    left = {"a": [1, 2]}
    right = {"a": [1, 3]}
    result = diff(left, right)
    assert result.changed == {"a[1]": {"old": 2, "new": 3}}


def test_diff_list_length_change():
    left = {"a": [1]}
    right = {"a": [1, 2]}
    result = diff(left, right)
    assert result.changed == {"a[1]": {"old": None, "new": 2}}


def test_diff_type_mismatch():
    left = {"a": 1}
    right = {"a": "1"}
    result = diff(left, right)
    assert result.changed == {"a": {"old": 1, "new": "1"}}


def test_diff_serialization():
    left = {"a": 1}
    right = {"a": 2}
    result = diff(left, right)
    payload = result.to_dict()
    assert payload == {"added": {}, "changed": {"a": {"old": 1, "new": 2}}, "removed": {}}


def test_dictdiff_no_common_keys():
    left = {"a": 1}
    right = {"b": 2}
    result = diff(left, right)
    assert result.added == {"b": 2}
    assert result.removed == {"a": 1}
    assert result.changed == {}


def test_diff_none_values():
    left = {"a": None}
    right = {"a": None}
    result = diff(left, right)
    assert result.is_empty() is True


def test_diff_complex_nested_mixed():
    left = {"a": {"b": [1, 2]}, "c": 3}
    right = {"a": {"b": [1, 2, 3]}, "c": 4}
    result = diff(left, right)
    assert result.changed == {"a.b[2]": {"old": None, "new": 3}, "c": {"old": 3, "new": 4}}
    assert result.added == {}
    assert result.removed == {}
