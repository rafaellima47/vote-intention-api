from __future__ import annotations

import sys
from pathlib import Path

import pytest


project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture
def database_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    db_path = tmp_path / "test_votes.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    return db_path
