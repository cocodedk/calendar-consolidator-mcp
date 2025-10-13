import { test, expect } from '@playwright/test';

test.describe('Dark Mode Visual Rendering', () => {
  test('should apply dark theme styles correctly', async ({ page }) => {
    await page.goto('/');

    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'dark');
    });

    await page.waitForTimeout(400);

    const bodyBg = await page.evaluate(() =>
      window.getComputedStyle(document.body).backgroundColor
    );
    expect(bodyBg).toMatch(/rgb\(26,\s*26,\s*26\)/);

    const headerBg = await page.evaluate(() =>
      window.getComputedStyle(document.querySelector('header')).backgroundColor
    );
    expect(headerBg).toMatch(/rgb\(45,\s*45,\s*45\)/);
  });

  test('should render all tabs correctly in dark mode', async ({ page }) => {
    await page.goto('/');

    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'dark');
    });

    const tabs = ['dashboard', 'sources', 'target', 'sync', 'logs', 'settings'];

    for (const tab of tabs) {
      await page.click(`.tab-btn[data-tab="${tab}"]`);
      await expect(page.locator(`#${tab}-tab`)).toBeVisible();

      const isVisible = await page.locator(`#${tab}-tab h2`).isVisible();
      expect(isVisible).toBe(true);
    }
  });

  test('should render cards with dark theme colors', async ({ page }) => {
    await page.goto('/');

    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'dark');
    });

    const cardBg = await page.evaluate(() => {
      const card = document.querySelector('.card');
      return card ? window.getComputedStyle(card).backgroundColor : null;
    });

    if (cardBg) {
      expect(cardBg).toMatch(/rgb\(45,\s*45,\s*45\)/);
    }
  });
});
