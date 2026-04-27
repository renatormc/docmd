from typing import TYPE_CHECKING

from docmd.filters.markdown_filter import MarkdownFilter
if TYPE_CHECKING:
    from docmd.core import RenderEnv

def markdown_filter(text: str) -> str:
    return text


def register(rend: 'RenderEnv') -> None:
    rend.jinja_env.filters["markdown"] = MarkdownFilter(rend)
