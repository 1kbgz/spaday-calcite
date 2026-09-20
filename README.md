<a href="https://github.com/1kbgz/spaday-calcite">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/1kbgz/spaday-calcite/raw/main/docs/img/logo-dark.webp?raw=true">
    <img alt="spaday-calcite logo, a faceted crystal inside a browser window" src="https://github.com/1kbgz/spaday-calcite/raw/main/docs/img/logo-light.webp?raw=true" width="800">
  </picture>
</a>

Typed [Calcite Design System](https://developers.arcgis.com/calcite-design-system/) components and browser assets for [spaday](https://github.com/1kbgz/spaday).

[![Build Status](https://github.com/1kbgz/spaday-calcite/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/spaday-calcite/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/spaday-calcite/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/spaday-calcite)
[![License](https://img.shields.io/github/license/1kbgz/spaday-calcite)](https://github.com/1kbgz/spaday-calcite)
[![PyPI](https://img.shields.io/pypi/v/spaday-calcite.svg)](https://pypi.python.org/pypi/spaday-calcite)

[![Preview of Calcite components in spaday](https://raw.githubusercontent.com/1kbgz/spaday-calcite/main/docs/img/preview.webp)](https://1kbgz.github.io/spaday-calcite/lite/)

## Usage

```python
from spaday import element
from spaday.backends.starlette import serve
from spaday_calcite import CalciteButton, CalciteNotice, package

page = element(
    "main",
    CalciteNotice(open=True, kind="success").child_in("title", "Ready"),
    CalciteButton("Open map", icon_start="map"),
)

app = serve(page, packages=[package], title="Calcite app")
```

Install the package with `pip install spaday-calcite`. Assets are loaded only when the exported `package` descriptor is passed to `serve`.

## Catalog coverage

Wrappers are generated from the Custom Elements Manifest published with `@esri/calcite-components` 5.1.2. The catalog covers its 104 public, declaratively usable elements. The upstream manifest also exposes `calcite-date-picker-day` and `calcite-date-picker-month`; these are undocumented private calendar renderers that require internal controller context and cannot be authored as standalone custom elements, so they are deliberately excluded.

Coverage is enforced at two layers:

- Python tests require the exact tags in `gallery.page.to_node()` to match the generated wrapper catalog.
- Playwright loads that Python page through Pyodide and requires every resulting host to be registered and hydrated with a shadow root.

The browser harness does not synthesize substitute components.

## Browser examples

- [Open the field operations workspace](https://1kbgz.github.io/spaday-calcite/lite/) ([source](spaday_calcite/example.py)).
- [Open the complete component gallery](https://1kbgz.github.io/spaday-calcite/lite/?example=gallery) ([source](spaday_calcite/gallery.py)).

Both run Python locally through Pyodide; no install or server is required.

## Run the examples locally

```bash
python -m pip install -e ".[examples]"
python -m spaday_calcite.example
python -m spaday_calcite.gallery
```

Open `http://127.0.0.1:8026` for the field operations workspace or `http://127.0.0.1:8027` for the complete component gallery.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
