import { expect, test } from "@playwright/test";

const PAGE = "http://127.0.0.1:8026";

test("renders the Python-authored field operations workspace", async ({
  page,
}) => {
  await page.goto(PAGE);
  await expect(page.locator(".hero h1")).toHaveText("Regional field atlas");
  await expect(page.locator("calcite-navigation")).toBeVisible();
  await expect(page.locator("calcite-card")).toHaveCount(3);
  await expect(page.locator("calcite-table-row")).toHaveCount(4);
  await expect(
    page.getByRole("button", { name: "Apply filters" }),
  ).toBeVisible();
});

test("keeps the workspace aligned on mobile", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto(PAGE);
  await expect(page.locator(".hero h1")).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    ),
  ).toBeLessThanOrEqual(1);
});
