/**
 * OAuth credentials section component for Settings tab.
 */

import { getCredentials } from './credentials_api.js';
import { createProviderCard } from './provider_card.js';
import { createIcloudCredentialsInfo } from './icloud_credentials.js';

export async function createCredentialsSection() {
    const section = document.createElement('div');
    section.className = 'settings-section credentials-section';
    section.id = 'oauth-credentials';

    section.innerHTML = `
        <h3>🔑 OAuth Credentials</h3>
        <p class="section-description">
            Configure OAuth application credentials for calendar providers.
            These are one-time setup credentials that enable users to connect their accounts.
        </p>
        <div id="credentials-content">
            <div class="loading">Loading credentials...</div>
        </div>
    `;

    // Load and display credentials
    loadCredentials(section);

    return section;
}

async function loadCredentials(section) {
    const content = section.querySelector('#credentials-content');

    try {
        const creds = await getCredentials();
        content.innerHTML = '';

        // Google credentials
        content.appendChild(createProviderCard('google', creds.google));

        // Microsoft credentials
        content.appendChild(createProviderCard('microsoft', creds.microsoft));

        // iCloud info
        content.appendChild(createIcloudCredentialsInfo());

    } catch (error) {
        content.innerHTML = `
            <div class="error-message">
                Failed to load credentials: ${error.message}
            </div>
        `;
    }
}
