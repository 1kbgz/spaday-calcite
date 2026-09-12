"""Browser gallery for every generated Calcite wrapper."""

from __future__ import annotations

import re

from spaday import SetProp, by_id, element
from spaday.backends.starlette import serve
from spaday.components.shell import App, Body, Main, Nav

from . import components as calcite, package

COMPONENT_NAMES = tuple(calcite.__all__)
COMPONENT_SNIPPETS = [f"from spaday_calcite import {name}" for name in COMPONENT_NAMES]


def _label(schema) -> str:
    return schema.tag.removeprefix("calcite-").replace("-", " ").title()


def _component(name: str):
    cls = getattr(calcite, name)
    schema = cls.schema
    props = {prop.name for prop in schema.props}
    label = _label(schema)
    values = {
        "description": "Live Python-generated preview",
        "full-name": "Ada Lovelace",
        "heading": label,
        "label": label,
        "label-text": label,
        "placeholder": "Enter a value",
        "text": label,
        "username": "ada",
    }
    kwargs = {key.replace("-", "_"): value for key, value in values.items() if key in props}
    kwargs.update(
        {
            "CalciteAction": {"icon": "layers", "text": label, "text_enabled": True},
            "CalciteAvatar": {"full_name": "Ada Lovelace", "username": "AL"},
            "CalciteButton": {"icon_start": "check"},
            "CalciteCheckbox": {"checked": True},
            "CalciteColorPicker": {"value": "#007ac2"},
            "CalciteColorPickerHexInput": {"value": "007ac2"},
            "CalciteColorPickerSwatch": {"color": "#007ac2"},
            "CalciteDatePicker": {"value": "2026-09-12"},
            "CalciteFab": {"icon": "plus", "text": "Create", "text_enabled": True},
            "CalciteFilter": {"value": "roads"},
            "CalciteGraph": {"min": 0, "max": 100},
            "CalciteIcon": {"icon": "map"},
            "CalciteInput": {"value": "ArcGIS", "type": "text"},
            "CalciteInputMessage": {"status": "valid"},
            "CalciteInputNumber": {"value": "42"},
            "CalciteInputText": {"value": "ArcGIS"},
            "CalciteInputTimePicker": {"value": "09:30"},
            "CalciteLink": {"href": "#catalog"},
            "CalciteLoader": {"inline": True, "text": "Loading"},
            "CalciteMeter": {"min": 0, "max": 100, "value": 64, "label": "Coverage"},
            "CalcitePagination": {"page_size": 10, "start_item": 1, "total_items": 96},
            "CalciteProgress": {"value": 0.64, "text": "64%"},
            "CalciteRadioButton": {"checked": True, "value": "selected"},
            "CalciteRating": {"value": 4, "count": 5},
            "CalciteSegmentedControlItem": {"checked": True, "value": "map"},
            "CalciteSlider": {"min": 0, "max": 100, "value": 64},
            "CalciteStepperItem": {"selected": True, "heading": label},
            "CalciteSwatch": {"color": "#007ac2", "value": "brand"},
            "CalciteSwitch": {"checked": True},
            "CalciteTableHeader": {"heading": label},
            "CalciteTimePicker": {"value": "09:30"},
        }.get(name, {})
    )
    component = cls(**kwargs)
    if name == "CalciteTree":
        return component.child(
            calcite.CalciteTreeItem("Transportation", expanded=True).child_in("children", calcite.CalciteTreeItem("Roads", selected=True)),
            calcite.CalciteTreeItem("Hydrology"),
        )
    if "" in schema.slots:
        component.text(label)
    return component


def _parent(name: str, component):
    c = calcite
    if name == "CalciteAccordionItem":
        return c.CalciteAccordion(component)
    if name == "CalciteAction":
        return c.CalciteActionBar(component)
    if name in {"CalciteAutocompleteItem", "CalciteAutocompleteItemGroup"}:
        return c.CalciteAutocomplete(component, open=True)
    if name in {"CalciteBlock", "CalciteBlockSection"}:
        return c.CalciteBlock(component, heading="Parent block", expanded=True)
    if name == "CalciteCard":
        return component.child_in("heading", "Card heading").child_in("description", "Card description")
    if name == "CalciteCardGroup":
        return component.child(c.CalciteCard().child_in("heading", "Grouped card"))
    if name == "CalciteCarouselItem":
        return c.CalciteCarousel(component)
    if name == "CalciteChipGroup":
        return component.child(c.CalciteChip("Brand", value="brand"))
    if name in {"CalciteComboboxItem", "CalciteComboboxItemGroup"}:
        return c.CalciteCombobox(component, placeholder="Choose a layer")
    if name in {"CalciteDropdownGroup", "CalciteDropdownItem"}:
        return c.CalciteDropdown(component, open=True).child_in("trigger", c.CalciteButton("Options"))
    if name == "CalciteFlowItem":
        return c.CalciteFlow(component)
    if name == "CalciteFocusTrap":
        return component.child(c.CalciteButton("Focusable control"))
    if name in {"CalciteListItem", "CalciteListItemGroup"}:
        return c.CalciteList(component)
    if name == "CalciteMenuItem":
        return c.CalciteMenu(component)
    if name == "CalciteNavigationLogo":
        return c.CalciteNavigation().child_in("logo", component)
    if name == "CalciteNavigationUser":
        return c.CalciteNavigation().child_in("user", component)
    if name in {"CalciteOption", "CalciteOptionGroup"}:
        return c.CalciteSelect(component, label="Layer type")
    if name == "CalciteRadioButton":
        return c.CalciteRadioButtonGroup(component, label_text="Map style")
    if name == "CalciteSegmentedControlItem":
        return c.CalciteSegmentedControl(component, label_text="View")
    if name == "CalciteShellPanel":
        return c.CalciteShell(element("main", "Map workspace")).child_in("panel-start", component)
    if name == "CalciteStepperItem":
        return c.CalciteStepper(component)
    if name == "CalciteSwatch":
        return c.CalciteSwatchGroup(component, label="Color")
    if name == "CalciteSwatchGroup":
        return component.child(c.CalciteSwatch(color="#007ac2", value="brand"))
    if name == "CalciteTab":
        return c.CalciteTabs(component).child_in("title-group", c.CalciteTabNav(c.CalciteTabTitle("Overview", selected=True)))
    if name == "CalciteTabNav":
        return c.CalciteTabs(c.CalciteTab("Overview", selected=True)).child_in(
            "title-group", component.child(c.CalciteTabTitle("Overview", selected=True))
        )
    if name == "CalciteTabTitle":
        return c.CalciteTabs(c.CalciteTab("Overview", selected=True)).child_in("title-group", c.CalciteTabNav(component))
    if name == "CalciteTableCell":
        return c.CalciteTable(c.CalciteTableRow(component))
    if name == "CalciteTableHeader":
        return c.CalciteTable(c.CalciteTableRow(component))
    if name == "CalciteTableRow":
        return c.CalciteTable(component.child(c.CalciteTableCell("Live row")))
    if name == "CalciteTile":
        return c.CalciteTileGroup(component, label="Layers")
    if name == "CalciteTileGroup":
        return component.child(c.CalciteTile(heading="Roads", description="Feature layer"))
    if name == "CalciteTreeItem":
        return c.CalciteTree(component)
    return component


OVERLAYS = {"CalciteActionMenu", "CalciteAlert", "CalciteDialog", "CalcitePopover", "CalciteSheet", "CalciteTooltip"}


def _preview(name: str):
    component = _component(name)
    if name in OVERLAYS:
        target_id = f"gallery-{re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()}"
        component.prop("id", target_id)
        if name in {"CalcitePopover", "CalciteTooltip"}:
            component.prop("reference-element", f"{target_id}-opener")
        if "" in component.schema.slots:
            component.text(f"Open {name.removeprefix('Calcite')}")
        opener = calcite.CalciteButton(id=f"{target_id}-opener").text(f"Open {name.removeprefix('Calcite')}")
        opener.on("click", SetProp(by_id(target_id), "open", True))
        return element("div", opener, component, class_="overlay-preview")
    return _parent(name, component)


catalog = element(
    "section",
    element("h2", "Complete Python catalog"),
    element("p", f"All {len(COMPONENT_NAMES)} generated Calcite wrappers render below."),
    element(
        "div",
        *(
            element(
                "article",
                element("h3", _label(getattr(calcite, name).schema)),
                element("code", f"from spaday_calcite import {name}"),
                element(
                    "div",
                    _preview(name),
                    class_="component-preview",
                    **{"data-component": getattr(calcite, name).tag},
                ),
                class_="gallery-card",
            )
            for name in COMPONENT_NAMES
        ),
        class_="catalog-grid",
        id="catalog",
    ),
)

page = App(
    Nav(element("strong", "spaday · Calcite"), calcite.CalciteChip("104 Python wrappers", kind="brand")),
    Body(
        Main(
            element(
                "header",
                element("span", "CALCITE DESIGN SYSTEM · PYTHON · PYODIDE", class_="eyebrow"),
                element("h1", "Component gallery"),
                element("p", "Real Calcite custom elements composed by Python and rendered in the browser."),
                class_="hero",
            ),
            catalog,
            class_="gallery-page",
        )
    ),
)

styles = """
<style>
  * { box-sizing: border-box; }
  body { margin: 0; color: var(--calcite-color-text-1); background: var(--calcite-color-background); font-family: var(--calcite-sans-family); }
  spa-nav { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: .8rem 1.2rem; background: var(--calcite-color-foreground-1); border-bottom: 1px solid var(--calcite-color-border-2); }
  .gallery-page { display: grid; gap: 2rem; width: min(100%, 96rem); margin: auto; padding: clamp(1rem, 3vw, 2.5rem); }
  .hero { padding: clamp(1.5rem, 4vw, 3.5rem); color: white; background: linear-gradient(135deg, #005e95, #009edb); border-radius: 1rem; box-shadow: 0 20px 50px #00304d33; }
  .hero h1 { margin: .35rem 0; font-size: clamp(2.4rem, 7vw, 5.5rem); line-height: .95; letter-spacing: -.05em; }
  .hero p { max-width: 50rem; margin: 1rem 0 0; font-size: 1.1rem; line-height: 1.6; }
  .eyebrow { font-size: .75rem; font-weight: 700; letter-spacing: .14em; }
  #catalog > p { color: var(--calcite-color-text-2); }
  .catalog-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
  .gallery-card { display: grid; align-content: start; gap: .7rem; min-width: 0; min-height: 13rem; padding: 1rem; overflow: visible; background: var(--calcite-color-foreground-1); border: 1px solid var(--calcite-color-border-2); border-radius: .65rem; box-shadow: var(--calcite-shadow-sm); }
  .gallery-card h3 { margin: 0; font-size: 1rem; }
  .gallery-card code { overflow: hidden; color: var(--calcite-color-text-2); font-size: .7rem; text-overflow: ellipsis; white-space: nowrap; }
  .component-preview { position: relative; display: grid; align-content: center; min-width: 0; min-height: 6rem; max-height: 18rem; overflow: auto; padding: .75rem; border: 1px dashed var(--calcite-color-border-2); }
  .component-preview[data-component="calcite-scrim"] { overflow: hidden; }
  .component-preview > *, .overlay-preview { max-width: 100%; }
  .overlay-preview { display: grid; gap: .5rem; }
  calcite-shell { display: block; min-height: 8rem; }
  calcite-graph, calcite-handle, calcite-sort-handle { display: block; min-height: 2rem; }
  @media (max-width: 900px) { .catalog-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 600px) { .catalog-grid { grid-template-columns: 1fr; } }
</style>
"""

app = serve(page, packages=[package], head=styles, title="spaday-calcite gallery")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8027)
