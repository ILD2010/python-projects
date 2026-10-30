"""Data models shared throughout Sentinel Lab."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any
from uuid import uuid4


class Severity(IntEnum):
    """Ordered alert levels; larger values indicate greater risk."""

    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

    @property
    def color(self) -> str:
        return {
            Severity.INFO: "cyan",
            Severity.LOW: "green",
            Severity.MEDIUM: "yellow",
            Severity.HIGH: "dark_orange",
            Severity.CRITICAL: "bold red",
        }[self]


@dataclass(slots=True)
class WebRequest:
    """A fictional HTTP request observed by the simulator."""

    source_ip: str
    method: str
    path: str
    status_code: int
    user_agent: str
    response_bytes: int
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    def summary(self) -> str:
        return f"{self.method} {self.path} -> {self.status_code}"


@dataclass(slots=True)
class Finding:
    """The result produced when one detection rule matches a request."""

    rule_name: str
    description: str
    score: int
    evidence: str
    recommendation: str


@dataclass(slots=True)
class Alert:
    """A scored collection of findings tied to one request."""

    request: WebRequest
    findings: list[Finding]
    score: int
    severity: Severity
    id: str = field(default_factory=lambda: uuid4().hex[:8].upper())
    status: str = "New"
    analyst_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.name
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Alert:
        return cls(
            id=data["id"],
            request=WebRequest(**data["request"]),
            findings=[Finding(**item) for item in data["findings"]],
            score=data["score"],
            severity=Severity[data["severity"]],
            status=data.get("status", "New"),
            analyst_note=data.get("analyst_note", ""),
        )

