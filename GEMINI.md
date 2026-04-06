# Simplenote Automation

A Python-based CLI tool for exporting Simplenote notes as Markdown files. This project uses `uv` for dependency management and `typer` for a modern CLI experience.

## Project Overview

- **Purpose:** Automate the fetching and filtering of notes from Simplenote to local Markdown files.
- **Main Technologies:**
    - **Python 3.13+**
    - **uv:** Package and project manager.
    - **Typer:** CLI framework.
    - **Rich:** Terminal formatting and progress bars.
    - **simplenote:** Python wrapper for the Simplenote API.
    - **python-dotenv:** Environment variable management.
    - **pytest:** Testing framework.

## Building and Running

### Prerequisites
Ensure you have `uv` installed. If not, follow the instructions at [astral.sh/uv](https://astral.sh/uv).

### Setup
1. **Sync Dependencies:**
   ```bash
   uv sync
   ```
2. **Configure Environment:**
   Copy `.env.template` to `.env` and provide your Simplenote credentials:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` with your `SIMPLENOTE_USERNAME` and `SIMPLENOTE_PASSWORD`.

### Key Commands
- **Fetch Notes:**
  ```bash
  uv run python main.py fetch [OPTIONS]
  ```
  Options include `-t/--tag`, `-o/--output`, `-s/--since`, `-q/--query`, and `--trashed`.
- **List Tags:**
  ```bash
  uv run python main.py list-tags
  ```
- **Run Tests:**
  ```bash
  uv run pytest
  ```

## Development Conventions

- **CLI Structure:** All CLI commands are defined in `main.py` using the `typer` library.
- **Configuration:** Credentials and default output directories are managed via `.env` files.
- **Filename Sanitization:** Notes are saved using their first line as the filename, sanitized by the `sanitize_filename` function to ensure cross-OS compatibility.
- **Testing:** Logic independent of the Simplenote API (like filename sanitization) is tested using `pytest` in `test_main.py`.
- **Dependency Management:** All dependencies are tracked in `pyproject.toml` and locked in `uv.lock`.
