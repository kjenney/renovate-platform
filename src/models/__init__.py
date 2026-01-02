"""Data models for Renovate Platform."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Repository:
    """Represents a repository being managed by Renovate."""

    id: int
    name: str
    url: str
    enabled: bool = True
    last_run: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class RenovateRun:
    """Represents a Renovate execution run."""

    id: int
    repository_id: int
    status: str  # pending, running, success, failed
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    log: Optional[str] = None
