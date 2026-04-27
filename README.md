# docmd

Convert markdown files to **docx** or **pdf** using `docxtpl` templates and LibreOffice headless.

## Installation

```bash
pip install docmd
```

Requires **Python 3.13+** and **LibreOffice** installed system-wide for PDF output.

## Usage

### CLI

```bash
docmd <folder> <output>
```

- `<folder>` — directory with your project files.
- `<output>` — output file (`.docx` or `.pdf`).

### Python API

```python
from docmd import convert

convert("my_project/", "output.docx")
convert("my_project/", "output.pdf")
```

## Input Folder Structure

```
my_project/
├── template.docx          # docxtpl template with Jinja2 placeholders
├── assets/                # Images to embed
│   ├── logo.png
│   └── photo.jpg
├── context.txt            # (optional) Variables one per line
├── intro.md               # One or more .md files
└── chapter-1.md
```

### `template.docx`

A standard Word document using [docxtpl](https://github.com/elapouya/python-docxtpl) syntax. Use Jinja2 placeholders like `{{ variable }}` or `{{ intro|markdown }}`.

### `context.txt`

Optional file with variables in `key = value` format, one per line:

```
author = John Doe
title = My Document
```

Lines starting with `#` and empty lines are ignored.

These variables are also available for substitution inside your `.md` files (see below).

### Markdown files

Every `.md` file is read and its content is injected into the template context. The variable name is the filename without extension (whitespace replaced by underscores):

| File | Context key |
|---|---|
| `intro.md` | `intro` |
| `chapter 1.md` | `chapter_1` |

You can use `{{ varname }}` inside `.md` files to reference values from `context.txt`:

**context.txt:**
```
name = John Doe
```

**intro.md:**
```markdown
# Hello {{ name }}
```

The result will be `# Hello John Doe`, then stored in context key `intro`.

Use the `markdown` filter in your template:

```jinja2
{{ intro|markdown }}
```

### Assets

All files inside `assets/` are listed in the `assets` context variable:

```json
{
  "logo": {"path": "assets/logo.png", "caption": ""},
  "photo": {"path": "assets/photo.jpg", "caption": ""}
}
```

Captions are empty for now (future: read from EXIF metadata).

## PDF Output

When the output path ends with `.pdf`, a docx is generated first and then converted to PDF via LibreOffice headless:

```bash
docmd my_project/ output.pdf
```

The intermediate docx file is automatically removed.

## License

MIT
