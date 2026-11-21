"""
DengsonBypass - CLI URL Unshortener, Tracker Cleaner & Security Inspector
Author : SIRO
GitHub : https://github.com/Jamz-colins
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from core.batch import (
    load_urls_from_file,
    process_batch,
    render_batch_table,
    save_results_to_file,
)
from core.clipboard import copy_to_clipboard
from core.domains import KNOWN_SHORTENERS, REDIRECT_WRAPPERS
from core.router import LinkRouter, ResolutionResult

APP_NAME = "DengsonBypass"
APP_VERSION = "3.0.1"
AUTHOR = "SIRO"
GITHUB_URL = "https://github.com/Jamz-colins"

console = Console()

HERO_ART = r"""
  ____  _____ _   _  ____ ____   ___  _   _     ____  __   ______   _    ____ ____
 |  _ \| ____| \ | |/ ___/ ___| / _ \| \ | |   | __ ) \ \ / /  _ \ / \  / ___/ ___|
 | | | |  _| |  \| | |  _\___ \| | | |  \| |   |  _ \  \ V /| |_) / _ \ \___ \___ \
 | |_| | |___| |\  | |_| |___) | |_| | |\  |   | |_) |  | | |  __/ ___ \ ___) |__) |
 |____/|_____|_| \_|\____|____/ \___/|_| \_|   |____/   |_| |_| /_/   \_\____/____/

                  _..----.._
                .'   _  _   '.
               /    (o)(o)    \                 _.._
              |    .------.    |              .' __ '.
              |   /  \__/  \   |            /  (o)(o)  \
             /|  |          |  |\          |   .----.   |
            / |   \        /   | \        /|  | \__/ |  |\
           /  |    '------'    |  \      / |   '----'   | \
               \      ||      /            |    |  |    |
                '----_||_----'                 _|  |_
                    [Deng]                      [Son]
"""


def show_banner() -> None:
    total_domains = len(KNOWN_SHORTENERS) + len(REDIRECT_WRAPPERS)
    vt_active = "AKTIF (VT_API_KEY)" if os.environ.get("VT_API_KEY") else "HEURISTIK LOKAL"

    art_text = Text(HERO_ART.strip("\n"), style="bold cyan")
    meta_text = Text.from_markup(
        f"\n[bold white]Multi-Hop Unshortener • Tracker Cleaner • Phishing Inspector[/bold white] [dim](v{APP_VERSION})[/dim]\n"
        f"[dim]Author :[/dim] [bold yellow]{AUTHOR}[/bold yellow]   [dim]|[/dim]   "
        f"[dim]GitHub :[/dim] [underline blue]{GITHUB_URL}[/underline blue]\n"
        f"[dim]Engine :[/dim] [cyan]{total_domains}+ Domain[/cyan]   [dim]|[/dim]   "
        f"[dim]Scanner:[/dim] [green]{vt_active}[/green]"
    )

    combined = Text.assemble(art_text, "\n", meta_text)
    console.print(Panel.fit(combined, border_style="bright_cyan", padding=(1, 2)))


def render_resolution(result: ResolutionResult) -> None:
    # 1. Redirect Chain Visualizer
    tree = Tree(f"[bold cyan]Alur Redirect ({len(result.hops)} Hop)[/bold cyan]")
    for hop in result.hops:
        time_str = f"{hop.elapsed_ms:.0f} ms" if hop.elapsed_ms > 0 else "instan"
        badge_color = "green" if hop.method == "FINAL" else "yellow"
        tree.add(
            f"[bold]Hop {hop.step}[/bold] [[{badge_color}]{hop.method}[/{badge_color}]] "
            f"[dim]({time_str})[/dim] -> [white]{hop.url}[/white]"
        )
    console.print(Panel(tree, title="1. Redirect Chain Visualizer", border_style="cyan"))

    # 2. Tracking Cleaner & Safety Check Table
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column("Label", style="bold white", width=20)
    info_table.add_column("Value")

    if result.removed_trackers:
        tracker_str = (
            f"[yellow]{len(result.removed_trackers)} parameter dihapus:[/yellow] "
            + ", ".join(f"[dim]{p}[/dim]" for p in result.removed_trackers)
        )
    else:
        tracker_str = "[dim]URL sudah bersih (tidak ada parameter pelacak)[/dim]"

    safety_badge = f"[{result.safety.color}][{result.safety.level}][/{result.safety.color}]"
    safety_details = "; ".join(result.safety.findings)
    if result.safety.vt_summary:
        safety_details += f"\n[cyan]{result.safety.vt_summary}[/cyan]"

    info_table.add_row("Tracker Cleaner", tracker_str)
    info_table.add_row("Safety Check", f"{safety_badge} {safety_details}")

    console.print(
        Panel(
            info_table,
            title="2. Tracker Cleaner & Security Inspector",
            border_style="blue",
        )
    )

    # 3. Hasil Akhir & Auto-Clipboard
    copied, clip_info = copy_to_clipboard(result.final_url)
    clip_note = (
        f"[dim]✓ Otomatis disalin ke clipboard ({clip_info})[/dim]"
        if copied
        else f"[yellow]! Clipboard: {clip_info}[/yellow]"
    )

    console.print(
        Panel(
            f"[bold green]{result.final_url}[/bold green]\n{clip_note}",
            title=f"3. {APP_NAME} - URL Tujuan Bersih",
            border_style="green",
        )
    )


def process_single(router: LinkRouter, short_url: str) -> None:
    with console.status("[bold yellow]Menelusuri rantai redirect & memindai keamanan...[/bold yellow]"):
        try:
            result = router.bypass(short_url)
        except Exception as exc:
            console.print(
                Panel(
                    f"[bold red]Gagal memproses link:[/bold red]\n{exc}",
                    title="Error",
                    border_style="red",
                )
            )
            return

    render_resolution(result)


def process_file(router: LinkRouter, filepath: str) -> None:
    try:
        urls = load_urls_from_file(filepath)
    except FileNotFoundError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        return

    if not urls:
        console.print("[yellow]File kosong atau tidak berisi URL valid.[/yellow]")
        return

    console.print(f"[cyan]Memproses {len(urls)} URL dari {filepath}...[/cyan]\n")
    results = process_batch(router, urls, console)
    render_batch_table(results, console)

    valid_urls = [r.target_url for r in results if r.success and r.target_url]
    console.print(
        f"\n[bold]Ringkasan:[/bold] [green]{len(valid_urls)} berhasil[/green], "
        f"[red]{len(results) - len(valid_urls)} gagal[/red]."
    )

    if valid_urls:
        copied, info = copy_to_clipboard("\n".join(valid_urls))
        if copied:
            console.print(
                f"[bold cyan]✓ {len(valid_urls)} URL tujuan disalin ke clipboard ({info}).[/bold cyan]"
            )
        else:
            console.print(f"[yellow]! Gagal menyalin ke clipboard: {info}[/yellow]")

        if Confirm.ask("Simpan hasil ke file teks?", default=False):
            out_file = Prompt.ask("Nama file output", default="hasil_bypass.txt").strip()
            saved_path = save_results_to_file(results, out_file)
            console.print(f"[green]✓ Tersimpan di: {saved_path}[/green]")


def handle_input(router: LinkRouter, raw_input: str) -> None:
    cleaned = raw_input.strip().strip("\"'")
    if not cleaned:
        return

    if Path(cleaned).expanduser().is_file():
        process_file(router, cleaned)
    else:
        process_single(router, cleaned)


def main() -> None:
    router = LinkRouter()

    if len(sys.argv) > 1:
        handle_input(router, sys.argv[1])
        return

    show_banner()
    console.print("[dim]Tempel short link atau path file .txt (ketik 'q' untuk keluar).[/dim]")

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]Tempel link[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[yellow]Keluar dari {APP_NAME}.[/yellow]")
            break

        if user_input.lower() in {"q", "exit", "quit"}:
            console.print(f"[yellow]Keluar dari {APP_NAME}.[/yellow]")
            break

        handle_input(router, user_input)


if __name__ == "__main__":
    main()
