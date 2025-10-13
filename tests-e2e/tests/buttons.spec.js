import { test, expect } from '@playwright/test';

test.describe('Button Interactions', () => {
  test('should have Quick Sync button on dashboard', async ({ page }) => {
    await page.goto('/');
    
    // Check Quick Sync button exists
    const quickSyncBtn = page.locator('button:has-text("Quick Sync")');
    await expect(quickSyncBtn).toBeVisible();
    
    // Click it (it will fail in API but we just test the click works)
    await quickSyncBtn.click();
  });

  test('should have Add Source button in Sources tab', async ({ page }) => {
    await page.goto('/');
    await page.click('.tab-btn[data-tab="sources"]');
    
    // Check Add Source button exists
    const addSourceBtn = page.locator('button:has-text("Add Source")');
    await expect(addSourceBtn).toBeVisible();
    
    // Click it
    await addSourceBtn.click();
  });

  test('should have Set Target button in Target tab', async ({ page }) => {
    await page.goto('/');
    await page.click('.tab-btn[data-tab="target"]');
    
    // Check Set Target button exists
    const setTargetBtn = page.locator('button:has-text("Set Target")');
    await expect(setTargetBtn).toBeVisible();
    
    // Click it
    await setTargetBtn.click();
  });

  test('should have Preview and Sync buttons in Sync tab', async ({ page }) => {
    await page.goto('/');
    await page.click('.tab-btn[data-tab="sync"]');
    
    // Check Preview Sync button
    const previewBtn = page.locator('button:has-text("Preview Sync")');
    await expect(previewBtn).toBeVisible();
    
    // Check Sync Now button
    const syncBtn = page.locator('button:has-text("Sync Now")');
    await expect(syncBtn).toBeVisible();
    
    // Click Preview button
    await previewBtn.click();
  });

  test('should have Refresh button in Logs tab', async ({ page }) => {
    await page.goto('/');
    await page.click('.tab-btn[data-tab="logs"]');
    
    // Check Refresh button exists
    const refreshBtn = page.locator('button:has-text("Refresh")');
    await expect(refreshBtn).toBeVisible();
    
    // Click it
    await refreshBtn.click();
  });

  test('should have Save Settings button in Settings tab', async ({ page }) => {
    await page.goto('/');
    await page.click('.tab-btn[data-tab="settings"]');
    
    // Check Save Settings button exists
    const saveBtn = page.locator('button:has-text("Save Settings")');
    await expect(saveBtn).toBeVisible();
  });
});

