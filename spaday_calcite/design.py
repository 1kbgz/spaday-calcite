"""How Calcite renders spaday's generic controls (:mod:`spaday.ui`)."""

from spaday.ui import ControlSpec, Design, Open, Options, Part, Value, Wrap

_BUTTON_INTENTS = {
    "neutral": "neutral",
    "primary": "brand",
    "info": "brand",
    "success": "brand",
    "warning": "neutral",
    "danger": "danger",
}
_BUTTON_APPEARANCES = {"filled": "solid", "outline": "outline", "plain": "transparent"}
_ALERT_INTENTS = {
    "neutral": "neutral",
    "primary": "brand",
    "info": "info",
    "success": "success",
    "warning": "warning",
    "danger": "danger",
}
_SIZES = {"sm": "s", "md": "m", "lg": "l"}
_FIELD = {"disabled": "disabled", "required": "required", "readonly": "read-only", "name": "name", "size": "scale"}
_WRAP = Wrap(tag="div", props={"class": "ui-field"})
_LABEL = (Part(kind="attr", name="label-text"), Part(kind="attr", name="label"))
_HELP = Part(kind="sibling", tag="small", after=True)
_ERROR = Part(kind="attr", name="validation-message")
_INVALID = {"status": "invalid"}

DESIGN = Design(
    name="calcite",
    controls={
        "button": ControlSpec(
            tag="calcite-button",
            label=Part(kind="text"),
            props={"intent": "kind", "appearance": "appearance", "size": "scale", "disabled": "disabled", "name": "name"},
            values={"intent": _BUTTON_INTENTS, "appearance": _BUTTON_APPEARANCES, "size": _SIZES},
        ),
        "input": ControlSpec(
            tag="calcite-input",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": "placeholder", "type": "type"},
            values={"size": _SIZES},
            value=Value(event="calciteInputInput"),
        ),
        "textarea": ControlSpec(
            tag="calcite-text-area",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={
                **_FIELD,
                "placeholder": "placeholder",
                "rows": "rows",
                "minlength": "min-length",
                "maxlength": "max-length",
            },
            value=Value(event="calciteTextAreaInput"),
            values={"size": _SIZES},
        ),
        "number-input": ControlSpec(
            tag="calcite-input-number",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": "placeholder", "min": "min", "max": "max", "step": "step"},
            value=Value(event="calciteInputNumberInput", codec="number", encode="string"),
            values={"size": _SIZES},
        ),
        "date-input": ControlSpec(
            tag="calcite-input-date-picker",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "min": "min", "max": "max"},
            value=Value(event="calciteInputDatePickerChange"),
            values={"size": _SIZES},
        ),
        "checkbox": ControlSpec(
            tag="calcite-checkbox",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=Part(kind="sibling", tag="small", after=True),
            invalid=_INVALID,
            props={**_FIELD},
            value=Value(prop="checked", event="calciteCheckboxChange"),
            values={"size": _SIZES},
        ),
        "switch": ControlSpec(
            tag="calcite-switch",
            wrap=_WRAP,
            label=(Part(kind="attr", name="label-text-end"), Part(kind="attr", name="label")),
            help=_HELP,
            error=Part(kind="sibling", tag="small", after=True),
            invalid={"aria-invalid": "true"},
            props={"disabled": "disabled", "required": None, "readonly": None, "name": "name", "size": "scale"},
            value=Value(prop="checked", event="calciteSwitchChange"),
            values={"size": _SIZES},
        ),
        "select": ControlSpec(
            tag="calcite-select",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": None},
            options=Options(kind="children", tag="calcite-option", value="value", label="label", selected="selected"),
            value=Value(event="calciteSelectChange", codec="json", defer=True),
            values={"size": _SIZES},
        ),
        "slider": ControlSpec(
            tag="calcite-slider",
            wrap=_WRAP,
            label=Part(kind="attr", name="label-text"),
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={
                "disabled": "disabled",
                "required": "required",
                "readonly": None,
                "name": "name",
                "size": "scale",
                "min": "min",
                "max": "max",
                "step": "step",
            },
            value=Value(event="calciteSliderInput", codec="number"),
            values={"size": _SIZES},
        ),
        "radio-group": ControlSpec(
            tag="calcite-radio-button-group",
            wrap=_WRAP,
            label=Part(kind="attr", name="label-text"),
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={"disabled": "disabled", "required": "required", "readonly": None, "name": "name", "size": "scale"},
            options=Options(
                tag="calcite-radio-button",
                value="value",
                label="label-text",
                disabled="disabled",
                selected="checked",
                selection=True,
            ),
            value=Value(event="calciteRadioButtonGroupChange", state="selectedItem.value"),
            values={"size": _SIZES},
        ),
        "alert": ControlSpec(
            tag="calcite-notice",
            fixed={"open": True},
            label=Part(kind="slot", name="title"),
            props={"intent": "kind"},
            values={"intent": _ALERT_INTENTS},
            children_slot="message",
        ),
        "progress": ControlSpec(
            tag="calcite-progress",
            label=Part(kind="attr", name="label"),
            props={"max": None},
            value=Value(scale_by="max", scale_to=100, scale_default=1),
        ),
        "dialog": ControlSpec(
            tag="calcite-dialog",
            label=Part(kind="attr", name="heading"),
            open=Open(prop="open", event="calciteDialogClose"),
        ),
    },
)

__all__ = ["DESIGN"]
