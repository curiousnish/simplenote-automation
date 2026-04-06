# Simplenote Automation

A Python CLI tool to export your Simplenote notes as Markdown files with advanced filtering.

## Setup

1.  **Install dependencies** (using [uv](https://github.com/astral-sh/uv)):
    ```bash
    uv sync
    ```

2.  **Configure credentials**:
    Copy `.env.template` to `.env` and fill in your Simplenote credentials:
    ```bash
    cp .env.template .env
    ```
    Then edit `.env`:
    ```ini
    SIMPLENOTE_USERNAME=your_email@example.com
    SIMPLENOTE_PASSWORD=your_password
    SIMPLENOTE_OUTPUT_DIR=./notes
    ```

## Usage

You can run the tool using `uv run sn`:

### Fetch all notes
```bash
uv run sn fetch
```

### Fetch by tags
```bash
uv run sn fetch -t work -t todo
```

### Search by content
```bash
uv run sn fetch -q "important"
```

### Filter by date (last 7 days)
```bash
uv run sn fetch --since 7
```

### Change output directory
```bash
uv run sn fetch -o ./my_vault
```

### List your tags
```bash
uv run sn list-tags
```

## Options for `fetch`

- `-t, --tag`: Filter by tags (multiple allowed, OR logic).
- `-o, --output`: Output directory (defaults to `.env` or `./notes`).
- `-s, --since`: Fetch notes modified in the last N days.
- `-q, --query`: Filter notes by content (case-insensitive).
- `--overwrite / --no-overwrite`: Control whether to overwrite existing files (default: True).
- `--trashed`: Include notes currently in the trash (default: False).

## Testing

Run tests with `pytest`:
```bash
uv run pytest
```
