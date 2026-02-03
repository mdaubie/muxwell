"""Base Action classes."""

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from rich.console import Console

from ..mkv import MKVWrapper
from ..operations import Operation
from ..utils.files import collect_video_files


@dataclass
class ActionContext:
    """Context available during actions analysis."""

    target: Path
    console: Console

    @cached_property
    def mkv_wrapper(self) -> MKVWrapper:
        return MKVWrapper(self.console)

    @cached_property
    def video_files(self) -> list[Path]:
        return collect_video_files(self.target)


class Action(ABC):
    """Base class for high-level actions."""

    @abstractmethod
    def analyze(self, context: ActionContext) -> Mapping[Path, Sequence[Operation]]:
        """
        Analyze the context and return operations for each file.

        Returns:
            Dict mapping file path -> list of operations to apply
        """
        pass
