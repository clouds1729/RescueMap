import { expect, test } from "@playwright/test";

test("RescueMap shell loads core workflow panels", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("RescueMap")).toBeVisible();
  await expect(page.getByText("Run Vectorization")).toBeVisible();
  await expect(page.getByText("Tools")).toBeVisible();
  await expect(page.getByText("Download GeoJSON")).toBeVisible();
});
