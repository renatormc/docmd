from uuid import uuid4
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from docmd.core import RenderEnv
from docmd import config


class SubdocInternalFunc:
    def __init__(self, renv: 'RenderEnv', template: str) -> None:
        self.jenv = renv
        self.template = config.LIBDIR / "globals" / template
        if not self.template.exists():
            raise FileNotFoundError(f"Template not found: {self.template}")

    def __call__(self, relpath: str, **kwargs):
        temp_docx = self.jenv.temp_folder / f"{uuid4().hex}.docx"
        self.jenv.docx_renderer.render_docx(
            self.template,
            kwargs,
            temp_docx,
        )
        return self.jenv.tpl.new_subdoc(str(temp_docx))
