"""Sentinel Lab entry point."""

from pathlib import Path

from sentinel.analyzer import TrafficAnalyzer
from sentinel.dashboard import SentinelDashboard
from sentinel.generator import TrafficGenerator
from sentinel.store import AlertStore


def main() -> None:
    """Create the application's collaborating objects and start the UI."""
    data_file = Path(__file__).parent / "data" / "alerts.json"
    dashboard = SentinelDashboard(
        generator=TrafficGenerator(),
        analyzer=TrafficAnalyzer(),
        store=AlertStore(data_file),
    )
    dashboard.run()


if __name__ == "__main__":
    main()

