# docmd

Convert markdown files to **docx** or **pdf** using `docxtpl` templates and LibreOffice headless.

## Architecture

```
src/docmd/
├── __init__.py          # Public API: convert()
├── __main__.py          # CLI entry point (argparse)
├── core.py              # Core conversion logic
├── assets.py            # Asset (image) handling
├── filters.py           # Custom Jinja2 filters (markdown, etc.)
└── pdf.py               # PDF export via LibreOffice
```

## Public API

```python
def convert(
    folder: str | Path,   # Folder containing the project files
    output: str | Path,   # Output path — use .docx or .pdf extension
) -> Path
```

## Input Folder Structure

The `folder` parameter must contain:

```
my_project/
├── template.docx          # docxtpl template with Jinja2 placeholders
├── assets/                # Images to embed
│   ├── image1.png
│   └── image2.jpg
├── context.txt            # (optional) Variables one per line: varname = value
├── intro.md               # One or more .md files
└── chapter-1.md
```

## Context Building

All data below is merged and passed to `docxtpl.DocxTemplate.render()`:

### From `context.txt`
- Format: `varname = value` (one per line)
- Lines starting with `#`, empty lines, and lines without `=` are skipped.
- Parsed first so its variables are available for substitution in markdown files.

### From markdown files
- Every `.md` file is read and its content is processed through Jinja2 with the variables from `context.txt`.
- This means you can use `{{ varname }}` inside `.md` files to reference values from `context.txt`.
- After substitution, the result is added to the context.
- The variable name is the filename without extension, with whitespace replaced by underscores.
- Example: `intro.md` → context key `intro`, `chapter 1.md` → context key `chapter_1`.

### From assets folder
- All files inside `assets/` are listed.
- A context variable `assets` is created as a `dict[str, dict]`.
- Key: filename without extension. Value: `{"path": Path, "caption": ""}`.
- `caption` is empty for now (future: read from EXIF metadata).

### `markdown` Jinja2 filter
- A custom filter named `markdown` is registered in the docxtpl environment.
- For now it simply returns the raw markdown text unchanged.
- Future: it will parse markdown and return proper docx elements (paragraphs, headings, lists, images, etc.).

Example template usage:

```jinja2
{{ intro|markdown }}
```

## CLI (`__main__.py`)

Uses **argparse**:

```bash
docmd <folder> <output>
```

- `<folder>` — path to the input folder (see structure above).
- `<output>` — output file (`.docx` for docx, `.pdf` for pdf).

## Conventions

- Type hints everywhere, no `Any` unless strictly necessary.
- Use `pathlib.Path` for all file paths.
- Use `docxtpl.DocxTemplate` for template rendering.
- Use `subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", ...])` for pdf conversion.
- Business logic in `core.py`, I/O and assets in `assets.py`, pdf conversion in `pdf.py`.
- Main function `convert()` lives in `__init__.py` as the public entry point.

## Dependencies

- `docxtpl` — Jinja2-based docx template engine
- `python-magic` (optional) — MIME type detection for assets
- LibreOffice installed system-wide for PDF conversion

## Commands

- `uv run docmd <folder> <output>` — run the CLI
- `uv add <pkg>` — add a dependency
- `uv sync` — sync environment
- `uv run pytest` — run all tests
- `uv run pytest -v` — run tests verbosely
