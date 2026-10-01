"""Live tests: need the claude CLI and JA_LIVE=1. They never run in CI.

    JA_LIVE=1 python3 -m pytest tests/live -v -s

Without both, every test here is skipped with the reason printed.
"""
import os
import shutil

import pytest


def live_blocker():
    if os.environ.get("JA_LIVE") != "1":
        return "live tests are off: set JA_LIVE=1 to run them (they call a model and cost money)"
    if shutil.which("claude") is None:
        return "live tests need the claude CLI on PATH, and it was not found"
    return None


@pytest.fixture(autouse=True)
def _live_only():
    reason = live_blocker()
    if reason:
        pytest.skip(reason)
