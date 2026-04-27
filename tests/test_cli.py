import subprocess
import sys
from pathlib import Path


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "docmd", "--help"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "folder" in result.stdout
    assert "output" in result.stdout


def test_cli_missing_folder():
    result = subprocess.run(
        [sys.executable, "-m", "docmd", "/nonexistent", "out.docx"],
        capture_output=True, text=True,
    )
    assert result.returncode != 0


def test_cli_converts_docx(sample_project: Path, tmp_path: Path):
    output = tmp_path / "result.docx"
    result = subprocess.run(
        [sys.executable, "-m", "docmd", str(sample_project), str(output)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "Generated:" in result.stdout
    assert output.is_file()
    assert output.stat().st_size > 0
