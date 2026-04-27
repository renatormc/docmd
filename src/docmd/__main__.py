import argparse
from pathlib import Path

from . import convert


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert markdown files to DOCX or PDF using a docxtpl template."
    )
    parser.add_argument("folder", type=Path, help="Folder containing the project files")
    parser.add_argument("output", type=Path, help="Output file (.docx or .pdf)")
    args = parser.parse_args()

    if not args.folder.is_dir():
        parser.error(f"folder not found: {args.folder}")

    result = convert(args.folder, args.output)
    print(f"Generated: {result}")


if __name__ == "__main__":
    main()
