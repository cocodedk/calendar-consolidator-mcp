import { test, expect } from '@playwright/test';

test.describe('Dark Mode System Preference', () => {
  test('should respect system dark preference on first load', async ({ page, context }) => {
    await context.clearCookies();
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());

    await page.emulateMedia({ colorScheme: 'dark' });
    await page.reload();

    const theme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );
    expect(theme).toBe('dark');

    await expect(page.locator('#theme-toggle .theme-icon')).toContainText('☀️');
  });

  test('should start in light mode with light system preference', async ({ page, context }) => {
    await context.clearCookies();
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());

    await page.emulateMedia({ colorScheme: 'light' });
    await page.reload();

    const theme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );
    expect(theme).toBe('light');

    await expect(page.locator('#theme-toggle .theme-icon')).toContainText('🌙');
  });

  test('should persist theme preference in localStorage', async ({ page }) => {
    await page.goto('/');

    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    });

    await page.reload();

    const theme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );
    expect(theme).toBe('dark');

    const storedTheme = await page.evaluate(() =>
      localStorage.getItem('theme')
    );
    expect(storedTheme).toBe('dark');
  });
});
