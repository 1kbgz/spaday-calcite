import asyncio
import re

import httpx

from spaday_calcite import gallery, package


def _tags(value):
    if isinstance(value, dict):
        if isinstance(value.get("tag"), str):
            yield value["tag"]
        for child in value.values():
            yield from _tags(child)
    elif isinstance(value, list):
        for child in value:
            yield from _tags(child)


def test_python_tree_contains_every_generated_component_and_snippet():
    expected_names = set(gallery.COMPONENT_NAMES)
    expected_tags = {schema.tag for schema in package.catalog}
    gallery_tags = {tag for tag in _tags(gallery.page.to_node()) if tag.startswith("calcite-")}
    snippet_names = set(re.findall(r"\bCalcite[A-Z][A-Za-z]+\b", "\n".join(gallery.COMPONENT_SNIPPETS)))

    assert gallery_tags == expected_tags
    assert snippet_names == expected_names


def test_gallery_app_serves_python_component_tree():
    async def request():
        transport = httpx.ASGITransport(app=gallery.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/tree.json")

    response = asyncio.run(request())
    assert response.status_code == 200
    assert "calcite-tree-item" in response.text
