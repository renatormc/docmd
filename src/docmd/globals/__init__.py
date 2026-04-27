from typing import TYPE_CHECKING
from docmd.globals.subdoc_func import SubdocFunc
if TYPE_CHECKING:
    from docmd.core import RenderEnv

def register(renv: 'RenderEnv') -> None:
    renv.jinja_env.globals["subdoc"] = SubdocFunc(renv)

