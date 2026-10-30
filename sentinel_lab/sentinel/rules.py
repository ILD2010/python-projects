"""Individual defensive detection rules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from urllib.parse import unquote_plus

from sentinel.models import Finding, WebRequest


class DetectionRule(ABC):
    """Interface implemented by every detection rule."""

    @abstractmethod
    def inspect(self, request: WebRequest) -> Finding | None:
        """Return a finding when the request matches, otherwise None."""


class InjectionPatternRule(DetectionRule):
    PATTERNS = ("' or ", "union select", "<script", "--")

    def inspect(self, request: WebRequest) -> Finding | None:
        decoded = unquote_plus(request.path).lower()
        matched = next((pattern for pattern in self.PATTERNS if pattern in decoded), None)
        if not matched:
            return None
        return Finding(
            rule_name="Injection pattern",
            description="Input resembles a SQL or browser-script injection attempt.",
            score=45,
            evidence=f"Decoded URL contains {matched!r}",
            recommendation="Validate input, use parameterized queries, and encode output.",
        )


class PathTraversalRule(DetectionRule):
    def inspect(self, request: WebRequest) -> Finding | None:
        decoded = unquote_plus(request.path).lower()
        if "../" not in decoded and "%2e" not in request.path.lower():
            return None
        return Finding(
            rule_name="Path traversal pattern",
            description="The path attempts to move outside the intended directory.",
            score=40,
            evidence=f"Suspicious path: {request.path}",
            recommendation="Resolve paths safely and enforce an allowed base directory.",
        )


class SensitiveResourceRule(DetectionRule):
    TARGETS = ("/.env", "/backup.zip", "/wp-login.php", "/admin")

    def inspect(self, request: WebRequest) -> Finding | None:
        target = next((item for item in self.TARGETS if request.path.startswith(item)), None)
        if not target:
            return None
        return Finding(
            rule_name="Sensitive resource probe",
            description="A commonly exposed administrative or secret file was requested.",
            score=28,
            evidence=f"Requested known probe target {target}",
            recommendation="Remove unused files and restrict administrative routes.",
        )


class AutomatedClientRule(DetectionRule):
    MARKERS = ("curl", "python-requests", "scanner")

    def inspect(self, request: WebRequest) -> Finding | None:
        agent = request.user_agent.lower()
        marker = next((item for item in self.MARKERS if item in agent), None)
        if not marker:
            return None
        return Finding(
            rule_name="Automated client",
            description="The client identifies itself as an automation tool.",
            score=12,
            evidence=f"User-Agent: {request.user_agent}",
            recommendation="Correlate with request rate before blocking automation.",
        )


class RejectedRequestRule(DetectionRule):
    def inspect(self, request: WebRequest) -> Finding | None:
        if request.status_code not in (401, 403):
            return None
        return Finding(
            rule_name="Access rejected",
            description="The server rejected authentication or authorization.",
            score=10,
            evidence=f"HTTP status {request.status_code}",
            recommendation="Check for repeated failures from the same source.",
        )


DEFAULT_RULES: tuple[DetectionRule, ...] = (
    InjectionPatternRule(),
    PathTraversalRule(),
    SensitiveResourceRule(),
    AutomatedClientRule(),
    RejectedRequestRule(),
)

