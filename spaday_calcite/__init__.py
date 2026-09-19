import json
from pathlib import Path

from spaday import ComponentPackage

from . import components as _components
from .components import *
from .components import __all__ as _component_names
from .design import DESIGN

__version__ = "0.1.0"

_EXTENSION = Path(__file__).parent / "extension"
_VERSIONS = _EXTENSION / "versions.json"

package = ComponentPackage(
    name="calcite",
    assets_dir=_EXTENSION,
    assets=(("css", "css/calcite.css"), ("js", "cdn/index.js")),
    components=tuple(getattr(_components, name) for name in _component_names),
    design=DESIGN,
    provides=json.loads(_VERSIONS.read_text(encoding="utf-8")) if _VERSIONS.exists() else {},
)

TOKENS = {
    "calcite_color_foreground_1": ("--calcite-color-foreground-1", "drives --spa-surface"),
    "calcite_color_foreground_2": ("--calcite-color-foreground-2", "drives --spa-surface-2"),
    "calcite_color_border_2": ("--calcite-color-border-2", "drives --spa-border"),
    "calcite_color_text_2": ("--calcite-color-text-2", "drives --spa-muted"),
    "calcite_color_brand": ("--calcite-color-brand", "drives --spa-accent"),
}

__all__ = [*_component_names, "DESIGN", "TOKENS", "package"]  # noqa: PLE0604
