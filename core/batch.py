from dataclasses import dataclass
from pathlib import Path
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table
from core.router import LinkRouter


@dataclass
class BatchResult:
    source_url: str
    target_url: str | None
    success: bool
    safety_level: str = "-"
    safety_color: str = "white"
    trackers_removed: int = 0
    error: str | None = None


def load_urls_from_file(filepath: str) -> list[str]:
    path = Path(filepath).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    urls: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#"):
                urls.append(cleaned)
    return urls


def process_batch(
    router: LinkRouter, urls: list[str], console: Console
) -> list[BatchResult]:
    results: list[BatchResult] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Memproses daftar link...", total=len(urls))

        for url in urls:
            progress.update(task, description=f"[cyan]Inspeksi:[/cyan] {url[:42]}...")
            try:
                res = router.bypass(url)
                results.append(
                    BatchResult(
                        source_url=url,
                        target_url=res.final_url,
                        success=True,
                        safety_level=res.safety.level,
                        safety_color=res.safety.color,
                        trackers_removed=len(res.removed_trackers),
                    )
                )
            except Exception as exc:
                results.append(
                    BatchResult(
                        source_url=url,
                        target_url=None,
                        success=False,
                        error=str(exc),
                    )
                )
            progress.advance(task)

    return results


def render_batch_table(results: list[BatchResult], console: Console) -> None:
    table = Table(title="Hasil Batch DengsonBypass", show_lines=True)
    table.add_column("No", justify="right", style="cyan", width=4)
    table.add_column("URL Asal", style="white", overflow="fold")
    table.add_column("Keamanan", justify="center", width=11)
    table.add_column("URL Tujuan (Bersih)", style="green", overflow="fold")

    for idx, item in enumerate(results, start=1):
        if item.success and item.target_url:
            badge = f"[{item.safety_color}]{item.safety_level}[/{item.safety_color}]"
            tracker_note = (
                f"\n[dim](-{item.trackers_removed} tracker dibersihkan)[/dim]"
                if item.trackers_removed > 0
                else ""
            )
            table.add_row(str(idx), item.source_url, badge, item.target_url + tracker_note)
        else:
            table.add_row(
                str(idx),
                item.source_url,
                "[bold red]GAGAL[/bold red]",
                f"[red]{item.error}[/red]",
            )

    console.print(table)


def save_results_to_file(results: list[BatchResult], output_path: str) -> Path:
    path = Path(output_path).expanduser()
    valid_targets = [r.target_url for r in results if r.success and r.target_url]
    path.write_text(
        "\n".join(valid_targets) + ("\n" if valid_targets else ""),
        encoding="utf-8",
    )
    return path
