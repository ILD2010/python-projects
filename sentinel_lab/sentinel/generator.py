"""Safe fictional traffic generation for the lab."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from sentinel.models import WebRequest


@dataclass
class TrafficGenerator:
    """Generates traffic scenarios without making real network requests."""

    randomizer: random.Random = field(default_factory=random.Random)

    NORMAL_PATHS = (
        "/", "/about", "/products", "/api/profile", "/login", "/assets/app.css"
    )
    USER_AGENTS = (
        "Mozilla/5.0 Firefox/143.0",
        "Mozilla/5.0 Chrome/140.0",
        "SentinelMobile/2.1",
    )
    SCENARIOS = ("normal", "injection", "traversal", "scanner", "auth_failure")

    def generate_batch(self, size: int = 30, suspicious_rate: float = 0.35) -> list[WebRequest]:
        requests: list[WebRequest] = []
        for _ in range(size):
            if self.randomizer.random() < suspicious_rate:
                scenario = self.randomizer.choice(self.SCENARIOS[1:])
            else:
                scenario = "normal"
            requests.append(self.generate(scenario))
        return requests

    def generate(self, scenario: str) -> WebRequest:
        factory = {
            "normal": self._normal,
            "injection": self._injection,
            "traversal": self._traversal,
            "scanner": self._scanner,
            "auth_failure": self._auth_failure,
        }.get(scenario)
        if factory is None:
            raise ValueError(f"Unknown scenario: {scenario}")
        return factory()

    def _ip(self, suspicious: bool = False) -> str:
        # RFC 5737 documentation ranges ensure these are never real targets.
        prefix = self.randomizer.choice(("192.0.2", "198.51.100", "203.0.113"))
        final = self.randomizer.randint(1, 254)
        if suspicious:
            final = self.randomizer.choice((13, 66, 99, 200))
        return f"{prefix}.{final}"

    def _request(self, **overrides: object) -> WebRequest:
        values: dict[str, object] = {
            "source_ip": self._ip(),
            "method": "GET",
            "path": self.randomizer.choice(self.NORMAL_PATHS),
            "status_code": 200,
            "user_agent": self.randomizer.choice(self.USER_AGENTS),
            "response_bytes": self.randomizer.randint(400, 9000),
        }
        values.update(overrides)
        return WebRequest(**values)  # type: ignore[arg-type]

    def _normal(self) -> WebRequest:
        status = self.randomizer.choices((200, 201, 304, 404), (70, 5, 15, 10))[0]
        return self._request(status_code=status)

    def _injection(self) -> WebRequest:
        path = self.randomizer.choice((
            "/search?q=%27+OR+1%3D1--",
            "/product?id=1+UNION+SELECT+demo",
            "/profile?name=%3Cscript%3Etraining%3C/script%3E",
        ))
        return self._request(source_ip=self._ip(True), path=path, status_code=403)

    def _traversal(self) -> WebRequest:
        path = self.randomizer.choice((
            "/download?file=../../demo/config.txt",
            "/static/%2e%2e/%2e%2e/training.txt",
        ))
        return self._request(source_ip=self._ip(True), path=path, status_code=403)

    def _scanner(self) -> WebRequest:
        return self._request(
            source_ip=self._ip(True),
            path=self.randomizer.choice(("/.env", "/admin", "/wp-login.php", "/backup.zip")),
            status_code=404,
            user_agent=self.randomizer.choice(("curl/8.0", "python-requests/2.x", "scanner-demo/1.0")),
        )

    def _auth_failure(self) -> WebRequest:
        return self._request(
            source_ip=self._ip(True),
            method="POST",
            path="/login",
            status_code=401,
            response_bytes=250,
        )

