import { test, expect } from '@playwright/test';

test.describe('Dashboard Elements', () => {
  test('should display system status section', async ({ page }) => {
    await page.goto('/');
    
    // Check System Status heading
    await expect(page.locator('h3:has-text("System Status")')).toBeVisible();
    
    // Check status stats are present
    await expect(page.locator('#active-sources-count')).toBeVisible();
    await expect(page.locator('#last-sync-time')).toBeVisible();
    await expect(page.locator('#error-count')).toBeVisible();
  });

  test('should display status bar', async ({ page }) => {
    await page.goto('/');
    
    // Check status bar exists
    const statusBar = page.locator('.status-bar');
    await expect(statusBar).toBeVisible();
    
    // Check status text
    const statusText = page.locator('#status-text');
    await expect(statusText).toBeVisible();
  });

  test('should have all tab buttons visible', async ({ page }) => {
    await page.goto('/');
    
    // Check all tab buttons
    await expect(page.locator('.tab-btn[data-tab="dashboard"]')).toBeVisible();
    await expect(page.locator('.tab-btn[data-tab="sources"]')).toBeVisible();
    await expect(page.locator('.tab-btn[data-tab="target"]')).toBeVisible();
    await expect(page.locator('.tab-btn[data-tab="sync"]')).toBeVisible();
    await expect(page.locator('.tab-btn[data-tab="logs"]')).toBeVisible();
    await expect(page.locator('.tab-btn[data-tab="settings"]')).toBeVisible();
  });

  test('should display dashboard card', async ({ page }) => {
    await page.goto('/');
    
    // Check card container
    const card = page.locator('#dashboard-tab .card');
    await expect(card).toBeVisible();
    
    // Check stat labels
    await expect(page.locator('label:has-text("Active Sources")')).toBeVisible();
    await expect(page.locator('label:has-text("Last Sync")')).toBeVisible();
    await expect(page.locator('label:has-text("Recent Errors")')).toBeVisible();
  });
});

