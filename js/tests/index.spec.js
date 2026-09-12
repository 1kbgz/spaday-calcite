import { expect, test } from "@playwright/test";

test("registers the complete Calcite catalog", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/dist/index.html");
  await page.waitForFunction(() => globalThis.__spadayCalcite?.tags.length);
  const result = await page.evaluate(() => ({
    count: globalThis.__spadayCalcite.tags.length,
    missing: globalThis.__spadayCalcite.tags.filter(
      (tag) => !customElements.get(tag),
    ),
  }));
  expect(result).toEqual({ count: 104, missing: [] });
  expect(errors).toEqual([]);
});

test("renders an upgraded Calcite component", async ({ page }) => {
  await page.goto("/dist/index.html");
  await page.evaluate(() => {
    const button = document.createElement("calcite-button");
    button.textContent = "Run";
    document.body.append(button);
  });
  await expect(page.locator("calcite-button")).toHaveText("Run");
  await expect
    .poll(() =>
      page.locator("calcite-button").evaluate((element) => ({
        hydrated: element.hasAttribute("calcite-hydrated"),
        shadow: !!element.shadowRoot,
      })),
    )
    .toEqual({ hydrated: true, shadow: true });
});

test("publishes the served Calcite version and shell palette", async ({
  page,
}) => {
  await page.goto("/dist/index.html");
  await page.waitForFunction(() => !!globalThis.__spadayCalcite);
  expect(await page.evaluate(() => globalThis.__spadayCalcite.version)).toBe(
    "5.1.2",
  );
  expect(
    await page.evaluate(() =>
      getComputedStyle(document.documentElement)
        .getPropertyValue("--spa-accent")
        .trim(),
    ),
  ).toBe("#007ac2");
});
