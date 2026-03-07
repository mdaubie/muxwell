"""Base Operation class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum

from ..mkv import MKVFile


class OperationPriority(IntEnum):
    ADD_TRACK = 10
    REMOVE_TRACK = 20
    SET_META = 30


class Operation(ABC):
    """Base class for all MKV operations."""

    priority: int = OperationPriority.SET_META

    def tie_breaker(self) -> tuple[int, ...]:
        # same-priority deterministic ordering
        return ()

    @property
    def sort_key(self) -> tuple[int, ...]:
        return (self.priority, *self.tie_breaker())

    def __lt__(self, other: Operation):
        return self.sort_key < other.sort_key

    @abstractmethod
    def apply(self, video: MKVFile):
        """Apply the operation to an MKV file."""
        pass
