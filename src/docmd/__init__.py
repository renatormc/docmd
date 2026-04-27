from pathlib import Path

from .core import run


def convert(folder: str | Path, output: str | Path) -> Path:
    return run(Path(folder), Path(output))
