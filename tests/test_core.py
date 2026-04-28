from pathlib import Path

from docmd.core import _build_context, DocxRenderer


def test_build_context_empty(tmp_path: Path):
    folder = tmp_path / "empty"
    folder.mkdir()
    ctx = _build_context(folder)
    assert ctx == {}


def test_build_context_md_files(sample_project: Path):
    ctx = _build_context(sample_project)
    assert ctx["intro"] == "# Introduction\nHello world."
    assert ctx["chapter_1"] == "## Chapter One\nContent here."


def test_build_context_context_txt(sample_project: Path):
    ctx = _build_context(sample_project)
    assert ctx["author"] == "John Doe"
    assert ctx["title"] == "My Doc"


def test_build_context_md_substitutes_vars(tmp_path: Path):
    folder = tmp_path / "proj"
    folder.mkdir()
    (folder / "context.txt").write_text("name = John\n", encoding="utf-8")
    (folder / "greeting.md").write_text("Hello {{ name }}!", encoding="utf-8")
    ctx = _build_context(folder)
    assert ctx["greeting"] == "Hello John!"


def test_build_context_context_txt_skips_invalid(tmp_path: Path):
    folder = tmp_path / "proj"
    folder.mkdir()
    (folder / "context.txt").write_text(
        "valid = yes\n\n=bad\nnoequal\nkey= value\n", encoding="utf-8"
    )
    ctx = _build_context(folder)
    assert ctx == {"valid": "yes", "key": "value"}


def test_build_context_assets(sample_project: Path):
    ctx = _build_context(sample_project)
    assets = ctx["assets"]
    assert isinstance(assets, dict)
    assert set(assets.keys()) == {"logo", "photo"}
    assert assets["logo"]["caption"] == ""
    assert assets["logo"]["path"].name == "logo.png"


def test_build_context_no_assets(tmp_path: Path):
    folder = tmp_path / "proj"
    folder.mkdir()
    (folder / "readme.md").write_text("# Hi", encoding="utf-8")
    ctx = _build_context(folder)
    assert "assets" not in ctx


def test_render_docx(template_path: Path, tmp_path: Path):
    output = tmp_path / "out.docx"
    context = {"name": "World"}
    r = DocxRenderer()
    result = r.render_docx(template_path, context, output)
    assert result == output
    assert output.is_file()
    assert output.stat().st_size > 0


def test_render_docx_with_markdown_filter(template_path: Path, tmp_path: Path):
    output = tmp_path / "out.docx"
    context = {"intro": "# Hello"}
    r = DocxRenderer()
    result = r.render_docx(template_path, context, output)
    assert result.is_file()
