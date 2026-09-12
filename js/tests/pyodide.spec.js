import fs from "fs";
import { expect, test } from "@playwright/test";

const built = fs.existsSync("dist/lite/index.html");

async function waitForPython(page) {
  await page.waitForFunction(
    () =>
      document.documentElement.dataset.ready === "true" ||
      document.querySelector("#pyodide-status")?.textContent ===
        "Unable to start",
    undefined,
    { timeout: 180_000 },
  );
  await expect(page.locator("html")).toHaveAttribute("data-ready", "true");
}

function collectErrors(page) {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  return errors;
}

test("runs the Calcite workspace from Python in Pyodide", async ({ page }) => {
  test.skip(!built, "run `make pyodide-example` first");
  test.setTimeout(240_000);
  const errors = collectErrors(page);
  await page.goto("/dist/lite/index.html");
  await waitForPython(page);
  await expect(page.locator(".hero h1")).toHaveText("Regional field atlas");
  await expect(page.locator("calcite-table")).toBeVisible();
  expect(errors).toEqual([]);
});

test("renders every Python wrapper in the Pyodide gallery", async ({
  page,
}) => {
  test.skip(!built, "run `make pyodide-example` first");
  test.setTimeout(240_000);
  await page.setViewportSize({ width: 1280, height: 900 });
  const errors = collectErrors(page);
  await page.goto("/dist/lite/?example=gallery");
  await waitForPython(page);
  await expect(page.locator(".hero h1")).toHaveText("Component gallery");
  await expect(page.locator(".gallery-card")).toHaveCount(104);

  const audit = await page.locator(".gallery-card").evaluateAll((cards) => ({
    invisiblePreviews: cards
      .filter((card) => {
        const preview = card.querySelector(".component-preview");
        if (!preview) return true;
        const rect = preview.getBoundingClientRect();
        const style = getComputedStyle(preview);
        return (
          rect.width === 0 ||
          rect.height === 0 ||
          style.display === "none" ||
          style.visibility === "hidden"
        );
      })
      .map((card) => card.querySelector("h3")?.textContent),
    missing: cards
      .filter((card) => {
        const tag = card.querySelector(".component-preview")?.dataset.component;
        return !tag || !card.querySelector(tag);
      })
      .map((card) => card.querySelector("h3")?.textContent),
    unupgraded: cards.flatMap((card) => {
      const tag = card.querySelector(".component-preview")?.dataset.component;
      const component = tag && card.querySelector(tag);
      return component && customElements.get(tag) && component.shadowRoot
        ? []
        : [tag];
    }),
  }));
  expect(audit).toEqual({
    invisiblePreviews: [],
    missing: [],
    unupgraded: [],
  });

  const scrimGeometry = await page
    .locator('.component-preview[data-component="calcite-scrim"]')
    .evaluate((preview) => {
      const scrim = preview.querySelector(":scope > calcite-scrim");
      const previewRect = preview.getBoundingClientRect();
      const scrimRect = scrim.getBoundingClientRect();
      return {
        contained:
          scrimRect.top >= previewRect.top &&
          scrimRect.right <= previewRect.right &&
          scrimRect.bottom <= previewRect.bottom &&
          scrimRect.left >= previewRect.left,
        offsetParentIsPreview: scrim.offsetParent === preview,
      };
    });
  expect(scrimGeometry).toEqual({
    contained: true,
    offsetParentIsPreview: true,
  });

  await expect(
    page.locator(
      '.component-preview[data-component="calcite-tree"] calcite-tree-item',
    ),
  ).toHaveCount(3);

  for (const name of [
    "action-menu",
    "alert",
    "dialog",
    "popover",
    "sheet",
    "tooltip",
  ]) {
    const id = `gallery-calcite-${name}`;
    await page.locator(`#${id}-opener`).evaluate((element) => element.click());
    await expect(page.locator(`#${id}`)).toHaveJSProperty("open", true);
    await page.locator(`#${id}`).evaluate((element) => {
      element.open = false;
    });
    await expect(page.locator(`#${id}`)).toHaveJSProperty("open", false);
  }

  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    ),
  ).toBeLessThanOrEqual(1);
  expect(errors).toEqual([]);
});
