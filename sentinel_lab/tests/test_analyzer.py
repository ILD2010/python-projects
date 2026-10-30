"""Tests for Sentinel Lab's detection engine."""

import unittest

from sentinel.analyzer import TrafficAnalyzer
from sentinel.models import Severity, WebRequest


def request(path: str, status: int = 200, agent: str = "Mozilla/5.0") -> WebRequest:
    return WebRequest(
        source_ip="192.0.2.10",
        method="GET",
        path=path,
        status_code=status,
        user_agent=agent,
        response_bytes=500,
    )


class TrafficAnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = TrafficAnalyzer()

    def test_normal_request_creates_no_alert(self) -> None:
        self.assertEqual(self.analyzer.analyze([request("/about")]), [])

    def test_injection_is_high_severity(self) -> None:
        alerts = self.analyzer.analyze([request("/search?q=%27+OR+1%3D1--", 403)])
        self.assertEqual(len(alerts), 1)
        self.assertGreaterEqual(alerts[0].severity, Severity.HIGH)

    def test_scanner_combines_multiple_findings(self) -> None:
        alerts = self.analyzer.analyze([request("/.env", 404, "scanner-demo/1.0")])
        self.assertEqual(len(alerts[0].findings), 2)
        self.assertEqual(alerts[0].score, 40)

    def test_alerts_are_sorted_by_score(self) -> None:
        alerts = self.analyzer.analyze([
            request("/login", 401),
            request("/download?file=../../demo.txt", 403),
        ])
        self.assertGreaterEqual(alerts[0].score, alerts[1].score)


if __name__ == "__main__":
    unittest.main()

