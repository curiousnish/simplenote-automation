import os
import re
import time
import typer
from typing import List, Optional
from simplenote import Simplenote
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress

app = typer.Typer(help="Simplenote automation CLI to fetch and manage notes.")
console = Console()

def sanitize_filename(name: str) -> str:
    """Remove invalid characters for filenames and limit length."""
    # Remove characters that are generally invalid in filenames across OSs
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Remove non-printable characters and control characters
    name = "".join(c for c in name if c.isprintable())
    return name.strip()[:50] or "untitled"

def get_simplenote_client():
    """Initialize Simplenote client with credentials from environment variables."""
    load_dotenv()
    username = os.getenv("SIMPLENOTE_USERNAME")
    password = os.getenv("SIMPLENOTE_PASSWORD")
    if not username or not password:
        console.print("[red]Error: SIMPLENOTE_USERNAME and SIMPLENOTE_PASSWORD must be set in .env file.[/red]")
        console.print("You can use .env.template as a starting point.")
        raise typer.Exit(code=1)
    return Simplenote(username, password)

@app.command()
def fetch(
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Filter by tags (OR logic). Can be used multiple times."),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory for markdown files."),
    since_days: Optional[int] = typer.Option(None, "--since", "-s", help="Fetch notes modified in the last N days."),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query to filter notes by content (case-insensitive)."),
    overwrite: bool = typer.Option(True, help="Overwrite existing files with the same name."),
    include_trashed: bool = typer.Option(False, "--trashed", help="Include notes that are in the trash."),
):
    """
    Fetch notes from Simplenote and save them as Markdown files.
    """
    sn = get_simplenote_client()
    
    if not output_dir:
        output_dir = os.getenv("SIMPLENOTE_OUTPUT_DIR", "./notes")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        console.print(f"Created directory: [green]{output_dir}[/green]")

    with console.status("[bold green]Connecting to Simplenote and fetching note list...") as status:
        # get_note_list returns (notes, status)
        # tags filtering is handled by the library if tags is a list
        notes, status_code = sn.get_note_list(tags=tags or [])
        if status_code != 0:
            console.print(f"[red]Error: Failed to fetch note list (Status: {status_code}).[/red]")
            raise typer.Exit(code=1)

    if not notes:
        console.print("[yellow]No notes found matching the criteria.[/yellow]")
        return

    # Filter by trashed status
    if not include_trashed:
        notes = [n for n in notes if not n.get("deleted")]

    # Filter by date if requested
    if since_days is not None:
        cutoff = time.time() - (since_days * 86400)
        notes = [n for n in notes if n.get("modificationDate", 0) >= cutoff]

    # Filter by query if provided
    if query:
        q = query.lower()
        notes = [n for n in notes if q in n.get("content", "").lower()]

    if not notes:
        console.print("[yellow]No notes remaining after applying filters.[/yellow]")
        return

    console.print(f"Found [blue]{len(notes)}[/blue] notes to download.")

    with Progress() as progress:
        task = progress.add_task("[cyan]Processing notes...", total=len(notes))
        
        # Track filenames in this batch to avoid internal collisions
        used_filenames = set()

        for n in notes:
            # The library get_note_list(data=True) usually returns content.
            # If not, we fetch it.
            if "content" not in n or not n["content"]:
                note, sc = sn.get_note(n["key"])
                if sc != 0:
                    console.print(f"[yellow]Warning: Could not fetch full content for note {n['key']}[/yellow]")
                    progress.update(task, advance=1)
                    continue
            else:
                note = n
            
            content = note.get("content", "")
            # Title is the first line of the note
            title_line = content.split("\n")[0] if content else "untitled"
            base_filename = sanitize_filename(title_line)
            
            filename = f"{base_filename}.md"
            filepath = os.path.join(output_dir, filename)
            
            # Handle duplicate filenames in the same batch or on disk
            counter = 1
            while (filename in used_filenames) or (not overwrite and os.path.exists(filepath)):
                filename = f"{base_filename}_{counter}.md"
                filepath = os.path.join(output_dir, filename)
                counter += 1
            
            used_filenames.add(filename)
            
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                console.print(f"[red]Error writing {filename}: {e}[/red]")
            
            progress.update(task, advance=1)

    console.print(f"\n[bold green]Success![/bold green] Fetched [blue]{len(notes)}[/blue] notes to [magenta]{output_dir}[/magenta].")

@app.command()
def list_tags():
    """List all unique tags used in your Simplenote account."""
    sn = get_simplenote_client()
    with console.status("[bold green]Fetching tags...") as status:
        notes, status_code = sn.get_note_list()
        if status_code != 0:
            console.print("[red]Error fetching notes.[/red]")
            return
        
        all_tags = set()
        for n in notes:
            all_tags.update(n.get("tags", []))
            
    if not all_tags:
        console.print("No tags found.")
    else:
        console.print("Your tags:")
        for tag in sorted(all_tags):
            console.print(f"- {tag}")

if __name__ == "__main__":
    app()
