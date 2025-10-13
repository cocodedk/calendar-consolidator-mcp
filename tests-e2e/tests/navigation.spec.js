import { test, expect } from '@playwright/test';

test.describe('Tab Navigation', () => {
  test('should load the dashboard page', async ({ page }) => {
    await page.goto('/');

    // Check page title
    await expect(page).toHaveTitle(/Calendar Consolidator/);

    // Check header
    await expect(page.locator('h1')).toContainText('Calendar Consolidator');

    // Check dashboard tab is active
    await expect(page.locator('.tab-btn[data-tab="dashboard"]')).toHaveClass(/active/);

    // Check dashboard content is visible
    await expect(page.locator('#dashboard-tab')).toBeVisible();
  });

  test('should navigate to Sources tab', async ({ page }) => {
    await page.goto('/');
    
    // Click Sources tab
    await page.click('.tab-btn[data-tab="sources"]');
    
    // Check Sources tab is active
    await expect(page.locator('.tab-btn[data-tab="sources"]')).toHaveClass(/active/);
    
    // Check Sources content is visible
    await expect(page.locator('#sources-tab')).toBeVisible();
    await expect(page.locator('#sources-tab h2')).toContainText('Source Calendars');
  });

  test('should navigate to Target tab', async ({ page }) => {
    await page.goto('/');
    
    // Click Target tab
    await page.click('.tab-btn[data-tab="target"]');
    
    // Check Target tab is active
    await expect(page.locator('.tab-btn[data-tab="target"]')).toHaveClass(/active/);
    
    // Check Target content is visible
    await expect(page.locator('#target-tab')).toBeVisible();
    await expect(page.locator('#target-tab h2')).toContainText('Target Calendar');
  });

  test('should navigate to Sync tab', async ({ page }) => {
    await page.goto('/');
    
    // Click Sync tab
    await page.click('.tab-btn[data-tab="sync"]');
    
    // Check Sync tab is active
    await expect(page.locator('.tab-btn[data-tab="sync"]')).toHaveClass(/active/);
    
    // Check Sync content is visible
    await expect(page.locator('#sync-tab')).toBeVisible();
    await expect(page.locator('#sync-tab h2')).toContainText('Sync Operations');
  });

  test('should navigate to Logs tab', async ({ page }) => {
    await page.goto('/');
    
    // Click Logs tab
    await page.click('.tab-btn[data-tab="logs"]');
    
    // Check Logs tab is active
    await expect(page.locator('.tab-btn[data-tab="logs"]')).toHaveClass(/active/);
    
    // Check Logs content is visible
    await expect(page.locator('#logs-tab')).toBeVisible();
    await expect(page.locator('#logs-tab h2')).toContainText('Sync Logs');
  });

  test('should navigate to Settings tab', async ({ page }) => {
    await page.goto('/');
    
    // Click Settings tab
    await page.click('.tab-btn[data-tab="settings"]');
    
    // Check Settings tab is active
    await expect(page.locator('.tab-btn[data-tab="settings"]')).toHaveClass(/active/);
    
    // Check Settings content is visible
    await expect(page.locator('#settings-tab')).toBeVisible();
    await expect(page.locator('#settings-tab h2')).toContainText('Settings');
  });

  test('should switch between multiple tabs', async ({ page }) => {
    await page.goto('/');

    // Navigate through tabs
    await page.click('.tab-btn[data-tab="sources"]');
    await expect(page.locator('#sources-tab')).toBeVisible();

    await page.click('.tab-btn[data-tab="target"]');
    await expect(page.locator('#target-tab')).toBeVisible();

    await page.click('.tab-btn[data-tab="dashboard"]');
    await expect(page.locator('#dashboard-tab')).toBeVisible();
  });
});
