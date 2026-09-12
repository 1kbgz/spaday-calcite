"""Operations dashboard example built with Calcite components."""

from spaday import element
from spaday.backends.starlette import serve
from spaday.components.shell import App, Body, Main, Nav

from . import (
    CalciteAction,
    CalciteAvatar,
    CalciteButton,
    CalciteCard,
    CalciteChip,
    CalciteInputText,
    CalciteLabel,
    CalciteList,
    CalciteListItem,
    CalciteNavigation,
    CalciteNavigationLogo,
    CalciteNavigationUser,
    CalciteNotice,
    CalciteOption,
    CalcitePanel,
    CalciteProgress,
    CalciteSelect,
    CalciteTable,
    CalciteTableCell,
    CalciteTableHeader,
    CalciteTableRow,
    package,
)

navigation = (
    CalciteNavigation(
        CalciteAction(icon="layers", text="Layers", text_enabled=True),
        CalciteAction(icon="map", text="Map", text_enabled=True, active=True),
    )
    .child_in("logo", CalciteNavigationLogo(heading="Field Atlas", description="Regional operations"))
    .child_in("user", CalciteNavigationUser(full_name="Ada Lovelace", username="ada"))
)

metrics = element(
    "section",
    CalciteCard(
        CalciteChip("On track", kind="success"),
        CalciteProgress(value=0.78, text="78%"),
    )
    .child_in("heading", "Survey coverage")
    .child_in("description", "312 of 400 parcels reviewed"),
    CalciteCard(CalciteChip("12 open", kind="warning")).child_in("heading", "Field incidents").child_in("description", "Three require review today"),
    CalciteCard(CalciteAvatar(full_name="Regional crew", username="RC"))
    .child_in("heading", "Active crews")
    .child_in("description", "Eight teams currently reporting"),
    class_="metric-grid",
)

requests = CalcitePanel(
    CalciteNotice(open=True, kind="info", icon=True)
    .child_in("title", "Morning sync complete")
    .child_in("message", "Seven new inspection records are ready."),
    CalciteList(
        CalciteListItem(label="North corridor", description="Bridge inspection · 09:40", icon_start="car"),
        CalciteListItem(label="River district", description="Floodplain survey · 10:15", icon_start="pin"),
        CalciteListItem(label="West ridge", description="Trail assessment · 11:30", icon_start="walking"),
        selection_mode="single",
    ),
    heading="Today’s field queue",
    description="Assignments ordered by scheduled start",
)

table = CalciteTable(
    CalciteTableRow(
        CalciteTableHeader(heading="Area"),
        CalciteTableHeader(heading="Owner"),
        CalciteTableHeader(heading="Status"),
    ),
    CalciteTableRow(CalciteTableCell("North corridor"), CalciteTableCell("M. Chen"), CalciteTableCell("In progress")),
    CalciteTableRow(CalciteTableCell("River district"), CalciteTableCell("S. Patel"), CalciteTableCell("Scheduled")),
    CalciteTableRow(CalciteTableCell("West ridge"), CalciteTableCell("J. Ortiz"), CalciteTableCell("Ready")),
    bordered=True,
    striped=True,
    caption="Field assignments",
)

filters = CalcitePanel(
    CalciteLabel("Search", CalciteInputText(value="inspection", clearable=True)),
    CalciteLabel(
        "Region",
        CalciteSelect(
            CalciteOption(label="All regions", value="all", selected=True),
            CalciteOption(label="North", value="north"),
            CalciteOption(label="South", value="south"),
        ),
    ),
    CalciteButton("Apply filters", icon_start="filter", width="full"),
    heading="Workspace filters",
)

page = App(
    Nav(element("strong", "spaday · Calcite"), CalciteChip("Live operations", kind="brand")),
    Body(
        Main(
            navigation,
            element(
                "header",
                element("span", "FIELD OPERATIONS · SEPTEMBER 12", class_="eyebrow"),
                element("h1", "Regional field atlas"),
                element("p", "Coordinate surveys, incidents, and crews from one accessible workspace."),
                class_="hero",
            ),
            metrics,
            element("section", requests, filters, class_="workspace-grid"),
            table,
            class_="page",
        )
    ),
)

styles = """
<style>
  * { box-sizing: border-box; }
  body { margin: 0; color: var(--calcite-color-text-1); background: var(--calcite-color-background); font-family: var(--calcite-sans-family); }
  spa-nav { display: flex; align-items: center; justify-content: space-between; padding: .8rem 1.2rem; border-bottom: 1px solid var(--calcite-color-border-2); background: var(--calcite-color-foreground-1); }
  .page { display: grid; gap: 1rem; width: min(100%, 76rem); margin: auto; padding: 1rem 1rem 3rem; }
  calcite-navigation { position: sticky; z-index: 10; top: 0; }
  .hero { padding: clamp(1.5rem, 5vw, 3.5rem); color: white; background: linear-gradient(120deg, #004874, #007ac2 60%, #00a9ce); border-radius: .9rem; }
  .hero h1 { max-width: 14ch; margin: .4rem 0; font-size: clamp(2.2rem, 6vw, 4.5rem); line-height: .95; letter-spacing: -.045em; }
  .hero p { max-width: 40rem; margin: 1rem 0 0; font-size: 1.05rem; line-height: 1.6; }
  .eyebrow { font-size: .75rem; font-weight: 700; letter-spacing: .13em; }
  .metric-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
  calcite-card { width: 100%; }
  .workspace-grid { display: grid; grid-template-columns: minmax(0, 2fr) minmax(16rem, 1fr); gap: 1rem; align-items: start; }
  calcite-panel { border: 1px solid var(--calcite-color-border-2); }
  @media (max-width: 720px) { .metric-grid, .workspace-grid { grid-template-columns: 1fr; } }
</style>
"""

app = serve(page, packages=[package], head=styles, title="spaday-calcite example")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8026)
