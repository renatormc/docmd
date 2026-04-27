from pathlib import Path
import subprocess


def convert_to_pdf(docx_path: Path, pdf_path: Path) -> Path:
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            str(docx_path.resolve()),
            "--outdir",
            str(pdf_path.parent.resolve()),
        ],
        check=True,
        capture_output=True,
    )
    return pdf_path
