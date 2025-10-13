/**
 * Provider credentials card component.
 */

import { showCredentialsForm } from './credentials_form_handler.js';

export function createProviderCard(provider, credentials) {
    const card = document.createElement('div');
    card.className = 'provider-card';

    const configured = credentials.configured;
    const providerName = provider === 'google' ? 'Google Calendar' : 'Microsoft Outlook/365';
    const icon = provider === 'google' ? '📧' : '📅';

    card.innerHTML = `
        <div class="provider-header">
            <h4>${icon} ${providerName}</h4>
            <span class="status-badge ${configured ? 'configured' : 'not-configured'}">
                ${configured ? '✓ Configured' : 'Not Configured'}
            </span>
        </div>
        ${configured ? createConfiguredView(provider, credentials) : ''}
        <button class="btn btn-primary config-btn" data-provider="${provider}">
            ${configured ? 'Update' : 'Configure'} Credentials
        </button>
        <div class="form-container" style="display: none;"></div>
    `;

    // Setup configure button
    const btn = card.querySelector('.config-btn');
    const formContainer = card.querySelector('.form-container');

    btn.addEventListener('click', () => {
        showCredentialsForm(provider, credentials, formContainer, btn);
    });

    return card;
}

function createConfiguredView(provider, credentials) {
    let fields = '';

    if (provider === 'google') {
        fields = `
            <div class="cred-field">
                <span class="field-label">Client ID:</span>
                <code>${credentials.client_id}</code>
            </div>
            <div class="cred-field">
                <span class="field-label">Client Secret:</span>
                <code>${credentials.client_secret}</code>
            </div>
        `;
    } else if (provider === 'microsoft') {
        fields = `
            <div class="cred-field">
                <span class="field-label">Client ID:</span>
                <code>${credentials.client_id}</code>
            </div>
            <div class="cred-field">
                <span class="field-label">Tenant ID:</span>
                <code>${credentials.tenant_id}</code>
            </div>
            <div class="cred-field">
                <span class="field-label">Client Secret:</span>
                <code>${credentials.client_secret}</code>
            </div>
        `;
    }

    return `<div class="configured-creds">${fields}</div>`;
}
