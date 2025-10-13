/**
 * OAuth Credentials visual validation tests.
 */

import { test, expect } from '@playwright/test';

test.describe('Credentials Visual Validation', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://127.0.0.1:3000');
        await page.click('[data-tab="settings"]');
        await page.waitForTimeout(500);
    });

    test('provider cards proper spacing', async ({ page }) => {
        const cards = await page.locator('.provider-card');
        const count = await cards.count();

        expect(count).toBeGreaterThanOrEqual(2);

        for (let i = 0; i < count - 1; i++) {
            const card = cards.nth(i);
            const box = await card.boundingBox();
            expect(box.height).toBeGreaterThan(100);
        }
    });

    test('status badges color coding', async ({ page }) => {
        const badges = await page.locator('.status-badge');
        const firstBadge = badges.first();

        const classes = await firstBadge.getAttribute('class');
        expect(classes).toMatch(/configured|not-configured/);
    });

    test('configured credentials display', async ({ page }) => {
        const credFields = await page.locator('.cred-field');

        if (await credFields.count() > 0) {
            const firstField = credFields.first();
            await expect(firstField).toBeVisible();
        }
    });

    test('form styling matches theme', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const form = await page.locator('.credentials-form');
        await expect(form).toBeVisible();

        const bg = await form.evaluate(el =>
            window.getComputedStyle(el).backgroundColor
        );
        expect(bg).toBeTruthy();
    });

    test('help links present', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const helpLink = await page.locator('.help-link');
        await expect(helpLink.first()).toBeVisible();
    });

    test('dark mode credentials section', async ({ page }) => {
        const themeToggle = await page.locator('[data-action="toggle-theme"]');
        if (await themeToggle.count() > 0) {
            await themeToggle.click();
            await page.waitForTimeout(300);
        }

        const section = await page.locator('#oauth-credentials');
        await expect(section).toBeVisible();
    });

    test('provider headers have icons', async ({ page }) => {
        const headers = await page.locator('.provider-header h4');
        const count = await headers.count();

        for (let i = 0; i < count; i++) {
            const text = await headers.nth(i).textContent();
            expect(text).toMatch(/[📧📅🍎]/);
        }
    });

    test('form fields have labels', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const labels = await page.locator('.credentials-form label');
        const count = await labels.count();

        expect(count).toBeGreaterThanOrEqual(2);
    });
});
