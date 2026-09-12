import ast
from pathlib import Path

from spaday import element, generate
from spaday.bootstrap import bootstrap

from spaday_calcite import TOKENS, CalciteButton, CalciteInputText, package

ROOT = Path(__file__).parent.parent


def test_generated_components_serialize():
    node = element("div", CalciteButton("Save", appearance="solid"), CalciteInputText(value="Atlas")).to_node()
    children = node["slots"]["default"]
    assert [child["tag"] for child in children] == ["calcite-button", "calcite-input-text"]
    assert children[0]["props"]["appearance"] == {"Str": "solid"}


def test_catalog_covers_the_package():
    tags = {schema.tag for schema in package.catalog}
    assert {"calcite-button", "calcite-shell", "calcite-table", "calcite-tree"} <= tags
    assert len(tags) == 104
    assert "" in CalciteButton.schema.slots


def test_package_drives_bootstrap_asset_urls():
    html = bootstrap(packages=[package])
    assert 'href="/components/calcite/css/calcite.css"' in html
    assert 'src="/components/calcite/cdn/index.js"' in html


def test_tokens_match_css_kwargs():
    for kwarg, (prop, description) in TOKENS.items():
        assert prop == f"--{kwarg.replace('_', '-')}"
        assert description.startswith("drives --spa-")


def test_generated_catalog_is_current():
    fresh = generate(str(ROOT / "custom-elements.json"))
    assert ast.dump(ast.parse(fresh)) == ast.dump(ast.parse((ROOT / "components.py").read_text(encoding="utf-8")))
