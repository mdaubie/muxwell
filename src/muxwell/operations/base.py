"""Base Operation class."""

from abc import ABC, abstractmethod

from ..mkv import MKVFile


class Operation(ABC):
    """Base class for all MKV operations."""

    @abstractmethod
    def apply(self, video: MKVFile):
        """Apply the operation to an MKV file."""
        pass
