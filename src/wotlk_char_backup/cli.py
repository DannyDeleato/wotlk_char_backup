"""Command-line interface for WotLK Character Backup."""

import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import __version__

app = typer.Typer(
    name="wotlk-backup",
    help="Export WotLK character data from AoWoW installations",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"wotlk-backup version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """WotLK Character Backup - Export character data from AoWoW installations."""
    pass


@app.command()
def export(
    profile_url: str = typer.Argument(..., help="AoWoW profile URL"),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: character-name.json)",
    ),
    include: Optional[List[str]] = typer.Option(
        None,
        "--include",
        help="What to include: gear, achievements, mounts, pets, all",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "--exclude",
        help="What to exclude: gear, achievements, mounts, pets",
    ),
    compress: bool = typer.Option(
        False,
        "--compress",
        help="Compress output with gzip",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Verbose output",
    ),
) -> None:
    """Export character data from an AoWoW profile URL."""
    from .scraper import AoWoWScraper
    from .scraper.aowow import AoWowScraperError, ProfileNotFoundError
    from .exporters import JSONExporter
    from .config import ScrapingConfig

    try:
        console.print(f"[bold blue]WotLK Character Backup v{__version__}[/bold blue]")
        console.print()

        # Validate URL
        if not profile_url.startswith("http"):
            console.print("[red]Error: Profile URL must start with http:// or https://[/red]")
            raise typer.Exit(1)

        # Create scraping config
        config = ScrapingConfig()
        if verbose:
            console.print(f"[dim]Configuration:[/dim]")
            console.print(f"[dim]  - Delay: {config.delay}s[/dim]")
            console.print(f"[dim]  - Timeout: {config.timeout}s[/dim]")
            console.print(f"[dim]  - Retries: {config.retries}[/dim]")
            console.print()

        # Scrape profile
        console.print(f"[cyan]Fetching profile:[/cyan] {profile_url}")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Scraping character data...", total=None)

            with AoWoWScraper(config) as scraper:
                try:
                    character_export = scraper.scrape_profile(profile_url)
                except ProfileNotFoundError:
                    console.print("\n[red]Error: Profile not found[/red]")
                    console.print(
                        "[yellow]Make sure the URL is correct and the character exists[/yellow]"
                    )
                    raise typer.Exit(1)
                except AoWowScraperError as e:
                    console.print(f"\n[red]Scraping error: {e}[/red]")
                    raise typer.Exit(1)

            progress.update(task, completed=True)

        # Display scraped info
        console.print()
        console.print("[green]✓[/green] Character data scraped successfully")
        console.print()
        console.print(f"[bold]{character_export.character.name}[/bold]")
        console.print(
            f"Level {character_export.character.level} "
            f"{character_export.character.race} "
            f"{character_export.character.character_class}"
        )
        console.print(f"[dim]{character_export.character.realm} ({character_export.character.region})[/dim]")
        if character_export.character.guild:
            console.print(f"Guild: {character_export.character.guild}")

        # Show what was collected
        equipped_count = character_export.gear.equipped_slots()
        console.print()
        console.print(f"[cyan]Collected:[/cyan]")
        console.print(f"  - Gear: {equipped_count}/19 slots")
        console.print(f"  - Achievements: {len(character_export.achievements)}")
        console.print(f"  - Mounts: {len(character_export.mounts)}")
        console.print(f"  - Pets: {len(character_export.pets)}")

        # Export to JSON
        console.print()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Exporting to JSON...", total=None)

            exporter = JSONExporter(pretty=True, compress=compress)

            # Handle include/exclude filters
            if include or exclude:
                json_str = exporter.export_partial(
                    character_export, include=include, exclude=exclude
                )
                if output:
                    output.write_text(json_str, encoding="utf-8")
                    output_file = output
                else:
                    # Generate filename
                    char = character_export.character
                    from datetime import datetime

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{char.name}_{char.realm}_{timestamp}.json"
                    if compress:
                        filename += ".gz"
                    output_file = Path(filename)
                    output_file.write_text(json_str, encoding="utf-8")
            else:
                output_file = exporter.export_to_file(character_export, output)

            progress.update(task, completed=True)

        console.print()
        console.print(f"[green]✓[/green] Export complete: [bold]{output_file}[/bold]")

        # Show file size
        file_size = output_file.stat().st_size
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"

        console.print(f"[dim]File size: {size_str}[/dim]")

    except KeyboardInterrupt:
        console.print("\n[red]Cancelled by user[/red]")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
