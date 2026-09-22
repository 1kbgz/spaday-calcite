import { expect, test } from "@playwright/test";

const PAGE = "http://127.0.0.1:8034";

test("renders Calcite controls and explicit fallbacks", async ({ page }) => {
  await page.goto(PAGE);
  await page.locator("#dialog").waitFor({ state: "attached" });
  expect(
    await page.evaluate(() =>
      [
        "save",
        "name",
        "notes",
        "count",
        "date",
        "agree",
        "dark",
        "plan",
        "priority",
        "volume",
        "alert",
        "progress",
        "dialog",
      ].map((id) => document.getElementById(id).localName),
    ),
  ).toEqual([
    "calcite-button",
    "calcite-input",
    "calcite-text-area",
    "calcite-input-number",
    "calcite-input-date-picker",
    "calcite-checkbox",
    "calcite-switch",
    "calcite-select",
    "calcite-radio-button-group",
    "calcite-slider",
    "calcite-notice",
    "calcite-progress",
    "calcite-dialog",
  ]);
  await expect(page.locator("[data-ui-fallback]")).toHaveCount(0);
  await expect(page.locator("#progress")).toHaveJSProperty("value", 50);
  await expect(page.locator("#alert [slot=title]")).toHaveText("Portable");
  await expect(page.locator("#alert [slot=message]")).toContainText(
    "All controls use the same generic contract.",
  );
});

test("Calcite values round-trip through the shared store", async ({ page }) => {
  await page.goto(PAGE);
  const state = page.locator("#state");
  await page.locator("#name").evaluate((element) => {
    element.value = "Ada";
    element.dispatchEvent(new Event("calciteInputInput", { bubbles: true }));
  });
  await page.locator("#count").evaluate((element) => {
    element.value = "4";
    element.dispatchEvent(
      new Event("calciteInputNumberInput", { bubbles: true }),
    );
  });
  await page.getByRole("checkbox", { name: "Agree" }).check();
  await page.getByRole("switch", { name: "Dark" }).check();
  await page.locator("#priority calcite-radio-button").nth(1).click();
  await expect(state).toContainText("Ada||4|2026-09-14|true|true|basic|2|");
  await page.locator("#save").click();
  await expect(state).toContainText("|true|false");
});

test("dialog and validation state remain bound", async ({ page }) => {
  await page.goto(PAGE);
  const dialog = page.locator("#dialog");
  await expect(dialog).toHaveJSProperty("open", false);
  await page.locator("#open").click();
  await expect(dialog).toHaveJSProperty("open", true);
  await dialog.evaluate((element) => {
    element.open = false;
    element.dispatchEvent(new Event("calciteDialogClose"));
  });
  await expect(page.locator("#state")).toContainText("|false");
  await expect(page.locator("#email")).toHaveJSProperty("status", "invalid");
  await expect(page.locator("#email")).toHaveJSProperty(
    "validationMessage",
    "Required",
  );
});
