"""Global operations (affect entire file)."""

from ..mkv import MKVFile
from . import Operation


class SetTitle(Operation):
    """Set the title of an MKV file."""

    def __init__(self, title: str):
        self.title = title

    def apply(self, video: MKVFile):
        video.title = self.title
