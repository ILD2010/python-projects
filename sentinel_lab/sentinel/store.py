"""JSON persistence for alerts and analyst work."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from sentinel.models import Alert


@dataclass
class AlertStore:
    path: Path

    def save(self, alerts: list[Alert]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps([alert.to_dict() for alert in alerts], indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)

    def load(self) -> list[Alert]:
        if not self.path.exists():
            return []
        try:
            raw_data = json.loads(self.path.read_text(encoding="utf-8"))
            return [Alert.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Could not load alert data: {error}") from error

