/**
 * OAuth Credentials UI element tests.
 */

import { test, expect } from '@playwright/test';

test.describe('Credentials UI Elements', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://127.0.0.1:3000');
        await page.click('[data-tab="settings"]');
        await page.waitForTimeout(500);
    });

    test('settings tab shows credentials section', async ({ page }) => {
        const section = await page.locator('#oauth-credentials');
        await expect(section).toBeVisible();
    });

    test('credentials section has heading', async ({ page }) => {
        const heading = await page.locator('#oauth-credentials h3');
        await expect(heading).toContainText('OAuth Credentials');
    });

    test('google provider card visible', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await expect(googleCard).toBeVisible();
    });

    test('microsoft provider card visible', async ({ page }) => {
        const msCard = await page.locator('.provider-card:has-text("Microsoft Outlook")');
        await expect(msCard).toBeVisible();
    });

    test('icloud info panel visible', async ({ page }) => {
        const icloudInfo = await page.locator('.credentials-info:has-text("iCloud")');
        await expect(icloudInfo).toBeVisible();
    });

    test('provider status badges visible', async ({ page }) => {
        const badges = await page.locator('.status-badge');
        const count = await badges.count();
        expect(count).toBeGreaterThan(0);
    });

    test('configure buttons clickable', async ({ page }) => {
        const configButtons = await page.locator('.config-btn');
        const count = await configButtons.count();

        for (let i = 0; i < count; i++) {
            const btn = configButtons.nth(i);
            await expect(btn).toBeEnabled();
        }
    });

    test('section description present', async ({ page }) => {
        const description = await page.locator('.section-description');
        await expect(description).toBeVisible();
        await expect(description).toContainText('one-time setup');
    });

    test('help links present in forms', async ({ page }) => {
        const helpLinks = await page.locator('.help-link');
        const count = await helpLinks.count();
        expect(count).toBeGreaterThan(0);
    });
});
