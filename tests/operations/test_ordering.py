from __future__ import annotations

from pathlib import Path

from muxwell.operations import (
    AddSubtitles,
    RemoveTrack,
    SetTrackDefault,
    SetTrackLanguage,
)


def test_operation_sort_orders_by_priority_and_remove_track_descending_id(
    tmp_path: Path,
):
    operations = [
        SetTrackLanguage(2, "eng"),
        RemoveTrack(0),
        AddSubtitles(tmp_path),
        RemoveTrack(1),
    ]

    ordered = sorted(operations)

    assert ordered == [
        operations[2],  # AddSubtitles (priority 10)
        operations[3],  # RemoveTrack(1) (priority 20, tie-breaker -1)
        operations[1],  # RemoveTrack(0) (priority 20, tie-breaker 0)
        operations[0],  # SetTrackLanguage (priority 30)
    ]


def test_operation_sort_preserves_input_order_when_sort_keys_are_equal():
    first = SetTrackDefault(3, True)
    second = SetTrackLanguage(3, "fra")

    ordered = sorted([first, second])

    assert ordered == [first, second]
