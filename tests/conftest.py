from pathlib import Path

import pytest
from docx import Document


@pytest.fixture
def template_path(tmp_path: Path) -> Path:
    path = tmp_path / "template.docx"
    doc = Document()
    
    doc.save(str(path))
    return path


@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    folder = tmp_path / "project"
    folder.mkdir()

    doc = Document()
    doc.save(str(folder / "template.docx"))

    (folder / "intro.md").write_text("# Introduction\nHello world.", encoding="utf-8")
    (folder / "chapter 1.md").write_text("## Chapter One\nContent here.", encoding="utf-8")
    (folder / "context.txt").write_text("author = John Doe\ntitle = My Doc\n", encoding="utf-8")

    assets = folder / "assets"
    assets.mkdir()
    (assets / "logo.png").touch()
    (assets / "photo.jpg").touch()

    return folder
