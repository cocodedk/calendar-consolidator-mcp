import { test, expect } from '@playwright/test';

test.describe('Visual Elements', () => {
  test('should display header with emoji', async ({ page }) => {
    await page.goto('/');
    
    // Check header contains calendar emoji
    const header = page.locator('header h1');
    await expect(header).toContainText('📅');
    await expect(header).toContainText('Calendar Consolidator');
  });

  test('should have proper styling classes', async ({ page }) => {
    await page.goto('/');
    
    // Check main container
    await expect(page.locator('.container')).toBeVisible();
    
    // Check tabs navigation
    await expect(page.locator('nav.tabs')).toBeVisible();
    
    // Check tab buttons have proper classes
    const tabBtns = page.locator('.tab-btn');
    await expect(tabBtns).toHaveCount(6);
  });

  test('should show active state on tabs', async ({ page }) => {
    await page.goto('/');
    
    // Dashboard should be active initially
    await expect(page.locator('.tab-btn[data-tab="dashboard"]')).toHaveClass(/active/);
    
    // Click Sources tab
    await page.click('.tab-btn[data-tab="sources"]');
    
    // Sources should be active now
    await expect(page.locator('.tab-btn[data-tab="sources"]')).toHaveClass(/active/);
    
    // Dashboard should no longer be active
    await expect(page.locator('.tab-btn[data-tab="dashboard"]')).not.toHaveClass(/active/);
  });

  test('should display card elements properly', async ({ page }) => {
    await page.goto('/');
    
    // Check cards exist
    const cards = page.locator('.card');
    await expect(cards.first()).toBeVisible();
  });

  test('should have responsive layout elements', async ({ page }) => {
    await page.goto('/');
    
    // Check main structure
    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('nav')).toBeVisible();
    await expect(page.locator('main')).toBeVisible();
  });

  test('should display all content sections', async ({ page }) => {
    await page.goto('/');
    
    // Check all tab content exists (even if hidden)
    await expect(page.locator('#dashboard-tab')).toBeAttached();
    await expect(page.locator('#sources-tab')).toBeAttached();
    await expect(page.locator('#target-tab')).toBeAttached();
    await expect(page.locator('#sync-tab')).toBeAttached();
    await expect(page.locator('#logs-tab')).toBeAttached();
    await expect(page.locator('#settings-tab')).toBeAttached();
  });
});

