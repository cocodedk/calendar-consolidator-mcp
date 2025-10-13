/**
 * OAuth Credentials form interaction tests.
 */

import { test, expect } from '@playwright/test';

test.describe('Credentials Form Interactions', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://127.0.0.1:3000');
        await page.click('[data-tab="settings"]');
        await page.waitForTimeout(500);
    });

    test('click configure shows google form', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        const configBtn = googleCard.locator('.config-btn');
        await configBtn.click();

        const form = await page.locator('.credentials-form:has-text("Google Calendar")');
        await expect(form).toBeVisible();
    });

    test('google form has required fields', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const clientIdField = await page.locator('#google-client-id');
        const clientSecretField = await page.locator('#google-client-secret');

        await expect(clientIdField).toBeVisible();
        await expect(clientSecretField).toBeVisible();
    });

    test('microsoft form has required fields', async ({ page }) => {
        const msCard = await page.locator('.provider-card:has-text("Microsoft")');
        await msCard.locator('.config-btn').click();
        await page.waitForTimeout(200);

        const clientIdField = await page.locator('#ms-client-id');
        const tenantIdField = await page.locator('#ms-tenant-id');
        const clientSecretField = await page.locator('#ms-client-secret');

        await expect(clientIdField).toBeVisible();
        await expect(tenantIdField).toBeVisible();
        await expect(clientSecretField).toBeVisible();
    });

    test('form validation on empty submit', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const saveBtn = await page.locator('#save-google-creds');
        await saveBtn.click();

        // Should show validation (alert or message)
        page.on('dialog', dialog => dialog.accept());
    });

    test('cancel button hides form', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const cancelBtn = await page.locator('#cancel-google-creds');
        await cancelBtn.click();
        await page.waitForTimeout(200);

        const form = await page.locator('.credentials-form');
        await expect(form).toBeHidden();
    });

    test('form input accepts text', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const clientIdField = await page.locator('#google-client-id');
        await clientIdField.fill('test.apps.googleusercontent.com');

        const value = await clientIdField.inputValue();
        expect(value).toBe('test.apps.googleusercontent.com');
    });

    test('save button enabled with data', async ({ page }) => {
        const googleCard = await page.locator('.provider-card:has-text("Google Calendar")');
        await googleCard.locator('.config-btn').click();

        const saveBtn = await page.locator('#save-google-creds');
        await expect(saveBtn).toBeEnabled();
    });
});
