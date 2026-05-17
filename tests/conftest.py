"""Shared test fixtures for muxwell tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from rich.console import Console

from .fixtures import *  # noqa: F403


@pytest.fixture
def console() -> Console:
    """Return a Rich console for testing."""
    return Console(force_terminal=False, force_jupyter=False)


@pytest.fixture
def console_mock() -> Mock:
    return Mock()
