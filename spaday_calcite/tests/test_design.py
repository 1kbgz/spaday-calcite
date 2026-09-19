import json

from spaday import Alert, Button, Dialog, NumberInput, Progress, RadioGroup, Select, TextInput, ToggleSwitch, element, validate
from spaday.ui import conformance, resolve
from spaday.ui.design import _plain

from spaday_calcite import DESIGN, package


def _props(node: dict) -> dict:
    return {key: _plain(value) for key, value in node.get("props", {}).items()}


def _find(node: dict, tag: str) -> dict:
    if node["tag"] == tag:
        return node
    for children in node.get("slots", {}).values():
        for child in children:
            if isinstance(child, dict):
                try:
                    return _find(child, tag)
                except LookupError:
                    pass
    raise LookupError(tag)


def test_the_package_publishes_its_design():
    assert package.design is DESIGN
    assert set(DESIGN.controls) == {
        "button",
        "checkbox",
        "date-input",
        "dialog",
        "input",
        "number-input",
        "progress",
        "radio-group",
        "select",
        "slider",
        "switch",
        "textarea",
        "alert",
    }


def test_fields_and_buttons_map_to_calcite():
    button = resolve(Button(label="Save", intent="danger", appearance="plain", size="lg").to_node(), DESIGN)
    assert button["tag"] == "calcite-button"
    assert _props(button) == {"textContent": "Save", "kind": "danger", "appearance": "transparent", "scale": "l"}

    text = resolve(TextInput(label="Name", help="Hint", error="Bad", type="email").to_node(), DESIGN)
    control = _find(text, "calcite-input")
    assert _props(control) == {
        "label-text": "Name",
        "label": "Name",
        "validation-message": "Bad",
        "status": "invalid",
        "type": "email",
    }
    assert _props(text["slots"]["default"][-1]) == {"textContent": "Hint"}


def test_choices_switch_and_dialog_keep_calcite_state_contracts():
    select = _find(resolve(Select(label="Plan", options=["a", {"value": 2, "label": "Two"}], value=2).to_node(), DESIGN), "calcite-select")
    assert select["bindings"]["value"] == {
        "compute": {"expr": "lit", "value": 2},
        "mode": "one-way",
        "defer": True,
        "codec": "json",
    }
    assert [(option["tag"], _props(option)) for option in select["slots"]["default"]] == [
        ("calcite-option", {"value": '"a"', "label": "a"}),
        ("calcite-option", {"value": "2", "label": "Two", "selected": True}),
    ]

    switch = _find(resolve(ToggleSwitch(label="Dark").bind("value", "dark", mode="two-way").to_node(), DESIGN), "calcite-switch")
    assert switch["bindings"]["checked"] == {"field": "dark", "mode": "two-way", "event": "calciteSwitchChange"}

    dialog = resolve(Dialog(label="Confirm").bind("open", "open", mode="two-way").to_node(), DESIGN)
    assert dialog["tag"] == "calcite-dialog"
    assert _props(dialog) == {"heading": "Confirm"}
    assert dialog["bindings"] == {"open": {"field": "open", "mode": "two-way", "event": "calciteDialogClose"}}


def test_number_radio_alert_and_progress_preserve_the_generic_contracts():
    number = _find(resolve(NumberInput(label="Count", value=4).bind("value", "count", mode="two-way").to_node(), DESIGN), "calcite-input-number")
    assert _props(number)["value"] == "4"
    assert number["bindings"]["value"] == {
        "field": "count",
        "mode": "two-way",
        "event": "calciteInputNumberInput",
        "codec": "number",
        "encode": "string",
    }

    radio = _find(
        resolve(RadioGroup(label="Priority", options=[1, {"value": 2, "label": "High"}]).bind("value", "priority", mode="two-way").to_node(), DESIGN),
        "calcite-radio-button-group",
    )
    assert radio["bindings"]["value"] == {
        "field": "priority",
        "mode": "two-way",
        "event": "calciteRadioButtonGroupChange",
        "state": "selectedItem.value",
        "selection": {"tag": "calcite-radio-button", "value": "value", "selected": "checked"},
    }
    assert [_props(option) for option in radio["slots"]["default"]] == [
        {"value": 1, "label-text": "1"},
        {"value": 2, "label-text": "High"},
    ]

    alert = resolve(Alert(element("span").text("Details"), label="Notice", intent="warning").to_node(), DESIGN)
    assert _props(alert) == {"open": True, "kind": "warning"}
    assert _props(alert["slots"]["title"][0]) == {"slot": "title", "textContent": "Notice"}
    assert alert["slots"]["message"][0]["tag"] == "span"

    progress = resolve(Progress(label="Upload", value=25, max=50).to_node(), DESIGN)
    assert _props(progress) == {"label": "Upload", "value": 50.0}
    default_progress = resolve(Progress(label="Upload", value=0.5).to_node(), DESIGN)
    assert _props(default_progress) == {"label": "Upload", "value": 50.0}
    bound_progress = resolve(Progress(max=50).bind("value", "progress").to_node(), DESIGN)
    assert bound_progress["bindings"]["value"] == {"field": "progress", "mode": "one-way", "scale": 2.0}


def test_the_conformance_page_uses_calcite_for_every_control():
    node = resolve(conformance.page().to_node(), DESIGN)
    validate(node)
    rendered = json.dumps(node)
    assert '"tag": "ui-' not in rendered
    assert rendered.count("data-ui-fallback") == 0
