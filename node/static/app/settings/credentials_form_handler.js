/**
 * Form handler for credentials forms.
 */

import { updateCredentials } from './credentials_api.js';
import { createGoogleCredentialsForm } from './google_credentials.js';
import { createMicrosoftCredentialsForm } from './microsoft_credentials.js';

export async function showCredentialsForm(provider, credentials, container, btn) {
    btn.style.display = 'none';
    container.style.display = 'block';
    container.innerHTML = '';

    const onSave = async (newCreds) => {
        try {
            container.innerHTML = '<div class="loading">Saving...</div>';
            await updateCredentials(provider, newCreds);
            alert('Success: Credentials saved successfully');
            setTimeout(() => window.location.reload(), 1000);
        } catch (error) {
            alert(`Error: ${error.message}`);
            container.style.display = 'none';
            btn.style.display = 'block';
        }
    };

    const onCancel = () => {
        container.style.display = 'none';
        btn.style.display = 'block';
    };

    if (provider === 'google') {
        container.appendChild(createGoogleCredentialsForm(credentials, onSave, onCancel));
    } else if (provider === 'microsoft') {
        container.appendChild(createMicrosoftCredentialsForm(credentials, onSave, onCancel));
    }
}
