"""Detection orchestration and risk scoring."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from sentinel.models import Alert, Severity, WebRequest
from sentinel.rules import DEFAULT_RULES, DetectionRule


@dataclass
class TrafficAnalyzer:
    rules: tuple[DetectionRule, ...] = field(default_factory=lambda: DEFAULT_RULES)

    def analyze(self, requests: list[WebRequest]) -> list[Alert]:
        """Inspect a batch, then add correlation scores for repeated sources."""
        source_counts = Counter(request.source_ip for request in requests)
        alerts: list[Alert] = []

        for request in requests:
            findings = [finding for rule in self.rules if (finding := rule.inspect(request))]
            if not findings:
                continue

            score = sum(finding.score for finding in findings)
            if source_counts[request.source_ip] >= 4:
                score += 15
            score = min(score, 100)

            alerts.append(Alert(
                request=request,
                findings=findings,
                score=score,
                severity=self.severity_for(score),
            ))

        return sorted(alerts, key=lambda alert: alert.score, reverse=True)

    @staticmethod
    def severity_for(score: int) -> Severity:
        if score >= 70:
            return Severity.CRITICAL
        if score >= 50:
            return Severity.HIGH
        if score >= 30:
            return Severity.MEDIUM
        if score >= 15:
            return Severity.LOW
        return Severity.INFO

