from __future__ import annotations

from unittest.mock import MagicMock

from muxwell.mkv import MKVFile
from muxwell.operations.base import Operation


class DummyOperation(Operation):
    def apply(self, video: MKVFile):
        return super().apply(video)


def test_operation_base_apply_is_executable_via_super():
    video = MagicMock()

    result = DummyOperation().apply(video)

    assert result is None
