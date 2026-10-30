"""Rich-powered terminal interface for Sentinel Lab."""

from __future__ import annotations

from collections import Counter

from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from sentinel.analyzer import TrafficAnalyzer
from sentinel.generator import TrafficGenerator
from sentinel.models import Alert, Severity, WebRequest
from sentinel.store import AlertStore


class SentinelDashboard:
    def __init__(self, generator: TrafficGenerator, analyzer: TrafficAnalyzer, store: AlertStore):
        self.generator = generator
        self.analyzer = analyzer
        self.store = store
        self.console = Console()
        self.requests: list[WebRequest] = []
        try:
            self.alerts = store.load()
        except ValueError:
            self.alerts = []

    def run(self) -> None:
        while True:
            self.console.clear()
            self.console.print(self._header())
            self.console.print(self._metrics())
            self.console.print(self._alert_table())
            self.console.print("\n[bold cyan]1[/] Generate traffic  [bold cyan]2[/] Investigate alert  "
                               "[bold cyan]3[/] Filter view  [bold cyan]4[/] Reset  [bold cyan]5[/] Exit")
            choice = Prompt.ask("[bold]Command[/]", choices=["1", "2", "3", "4", "5"])

            if choice == "1":
                self._generate()
            elif choice == "2":
                self._investigate()
            elif choice == "3":
                self._filter()
            elif choice == "4":
                self._reset()
            else:
                self.store.save(self.alerts)
                self.console.print("[green]Investigation saved. Stay curious.[/]")
                return

    def _header(self) -> Panel:
        title = Text("SENTINEL LAB", style="bold bright_cyan", justify="center")
        subtitle = Text("Local Security Operations Simulator", style="dim", justify="center")
        return Panel(Align.center(Group(title, subtitle)), border_style="cyan")

    def _metrics(self) -> Table:
        counts = Counter(alert.severity for alert in self.alerts)
        open_count = sum(alert.status != "Resolved" for alert in self.alerts)
        table = Table.grid(expand=True)
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_row(
            f"[bold]{len(self.requests)}[/]\n[dim]REQUESTS[/]",
            f"[bold yellow]{len(self.alerts)}[/]\n[dim]ALERTS[/]",
            f"[bold red]{counts[Severity.CRITICAL]}[/]\n[dim]CRITICAL[/]",
            f"[bold cyan]{open_count}[/]\n[dim]OPEN CASES[/]",
        )
        return table

    def _alert_table(self, alerts: list[Alert] | None = None) -> Table:
        visible = self.alerts if alerts is None else alerts
        table = Table(title="Detection Queue", expand=True, border_style="blue")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Time", no_wrap=True)
        table.add_column("Source")
        table.add_column("Request", overflow="fold")
        table.add_column("Score", justify="right")
        table.add_column("Severity")
        table.add_column("Status")

        for alert in visible[:12]:
            table.add_row(
                alert.id,
                alert.request.timestamp[11:19],
                alert.request.source_ip,
                alert.request.summary(),
                str(alert.score),
                Text(alert.severity.name, style=alert.severity.color),
                alert.status,
            )
        if not visible:
            table.add_row("-", "-", "-", "Generate traffic to begin", "-", "-", "-")
        return table

    def _generate(self) -> None:
        size = IntPrompt.ask("Number of requests", default=30)
        size = max(5, min(size, 200))
        batch = self.generator.generate_batch(size)
        new_alerts = self.analyzer.analyze(batch)
        self.requests.extend(batch)
        self.alerts = new_alerts + self.alerts
        self.store.save(self.alerts)
        self.console.print(f"[green]Analyzed {size} requests and created {len(new_alerts)} alerts.[/]")
        Prompt.ask("Press Enter to continue", default="")

    def _find_alert(self, alert_id: str) -> Alert | None:
        return next((alert for alert in self.alerts if alert.id == alert_id.upper()), None)

    def _investigate(self) -> None:
        if not self.alerts:
            self.console.print("[yellow]There are no alerts to investigate.[/]")
            Prompt.ask("Press Enter to continue", default="")
            return

        alert_id = Prompt.ask("Alert ID")
        alert = self._find_alert(alert_id)
        if alert is None:
            self.console.print("[red]Alert not found.[/]")
            Prompt.ask("Press Enter to continue", default="")
            return

        self.console.clear()
        self.console.print(self._detail_panel(alert))
        action = Prompt.ask(
            "Set case status",
            choices=["New", "Investigating", "Resolved", "False Positive"],
            default=alert.status,
        )
        note = Prompt.ask("Analyst note", default=alert.analyst_note)
        alert.status = action
        alert.analyst_note = note
        self.store.save(self.alerts)
        self.console.print("[green]Case updated.[/]")
        Prompt.ask("Press Enter to continue", default="")

    def _detail_panel(self, alert: Alert) -> Panel:
        request = alert.request
        lines = [
            Text(f"Alert {alert.id} — {alert.severity.name} ({alert.score}/100)", style=alert.severity.color),
            Text(f"Source: {request.source_ip}"),
            Text(f"Request: {request.summary()}"),
            Text(f"User-Agent: {request.user_agent}"),
            Text(""),
        ]
        for index, finding in enumerate(alert.findings, 1):
            lines.extend((
                Text(f"{index}. {finding.rule_name}", style="bold yellow"),
                Text(f"   Why: {finding.description}"),
                Text(f"   Evidence: {finding.evidence}"),
                Text(f"   Defense: {finding.recommendation}", style="green"),
            ))
        return Panel(Group(*lines), title="Incident Investigation", border_style=alert.severity.color)

    def _filter(self) -> None:
        choice = Prompt.ask(
            "Minimum severity",
            choices=[level.name for level in Severity],
            default="MEDIUM",
        )
        minimum = Severity[choice]
        visible = [alert for alert in self.alerts if alert.severity >= minimum]
        self.console.clear()
        self.console.print(self._alert_table(visible))
        Prompt.ask("Press Enter to return", default="")

    def _reset(self) -> None:
        if Prompt.ask("Delete current lab session?", choices=["y", "n"], default="n") == "y":
            self.requests.clear()
            self.alerts.clear()
            self.store.save([])

