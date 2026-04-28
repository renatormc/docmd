import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from docxtpl import DocxTemplate
from jinja2 import Environment, Template

from .assets import collect_assets
from .filters import register as register_filters
from .globals import register as register_globals


def _parse_context_txt(folder: Path) -> dict:
    context: dict = {}
    ctx_file = folder / "context.txt"
    if not ctx_file.is_file():
        return context
    for line in ctx_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if not key:
            continue
        context[key] = val.strip()
    return context


def _build_context(folder: Path) -> dict:
    ctx_vars = _parse_context_txt(folder)

    for md_file in sorted(folder.glob("*.md")):
        key = md_file.stem.replace(" ", "_")
        content = md_file.read_text(encoding="utf-8")
        content = Template(content).render(ctx_vars)
        ctx_vars[key] = content

    assets_path = folder / "assets"
    if assets_path.is_dir():
        ctx_vars["assets"] = collect_assets(assets_path)

    return ctx_vars

@dataclass
class RenderEnv:
    tpl: DocxTemplate
    jinja_env: Environment
    temp_folder: Path
    assets_folder: Path
    docx_renderer: 'DocxRenderer'


class DocxRenderer:
    def render_docx(self, template_path: Path, context: dict, output_path: Path) -> Path:
        temp_folder = Path(tempfile.mkdtemp(prefix="docmd_"))
        renv = RenderEnv(
            tpl=DocxTemplate(str(template_path)),
            jinja_env=Environment(),
            temp_folder=temp_folder,
            assets_folder=template_path.parent / "assets",
            docx_renderer=self,
        )
        try:
            register_filters(renv)
            register_globals(renv)
            renv.tpl.render(context, jinja_env=renv.jinja_env)
            renv.tpl.save(str(output_path))
            return output_path
        finally:
            shutil.rmtree(temp_folder, ignore_errors=True)


def run(folder: Path, output: Path) -> Path:
    template_path = folder / "template.docx"
    if not template_path.is_file():
        
        raise FileNotFoundError(f"template.docx not found in {folder}")

    context = _build_context(folder)

    r = DocxRenderer()

    if output.suffix == ".pdf":
        docx_path = output.with_suffix(".docx")
        
        r.render_docx(template_path, context, docx_path)
        from .pdf import convert_to_pdf

        result = convert_to_pdf(docx_path, output)
        # docx_path.unlink()
        return result

    return r.render_docx(template_path, context, output)
