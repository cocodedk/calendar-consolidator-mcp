import { test, expect } from '@playwright/test';

test.describe('Dark Mode Toggle', () => {
  test('should toggle theme when button is clicked', async ({ page }) => {
    await page.goto('/');

    const initialTheme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );

    await page.click('#theme-toggle');
    await page.waitForTimeout(100);

    const newTheme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );
    expect(newTheme).not.toBe(initialTheme);
  });

  test('should update toggle button icon when theme changes', async ({ page }) => {
    await page.goto('/');

    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await page.reload();

    await expect(page.locator('#theme-toggle .theme-icon')).toContainText('🌙');

    await page.click('#theme-toggle');
    await page.waitForTimeout(100);

    await expect(page.locator('#theme-toggle .theme-icon')).toContainText('☀️');
  });

  test('should have accessible aria-label on toggle button', async ({ page }) => {
    await page.goto('/');

    const ariaLabel = await page.getAttribute('#theme-toggle', 'aria-label');
    expect(ariaLabel).toBeTruthy();
    expect(ariaLabel).toMatch(/dark mode|light mode/i);
  });

  test('should maintain theme when navigating between tabs', async ({ page }) => {
    await page.goto('/');

    await page.click('#theme-toggle');
    await page.waitForTimeout(100);

    const theme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );

    await page.click('.tab-btn[data-tab="sources"]');
    await page.click('.tab-btn[data-tab="target"]');
    await page.click('.tab-btn[data-tab="sync"]');

    const themeAfterNav = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );
    expect(themeAfterNav).toBe(theme);
  });
});
