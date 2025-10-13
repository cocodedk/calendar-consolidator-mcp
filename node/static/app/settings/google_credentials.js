/**
 * Google credentials form component.
 */

export function createGoogleCredentialsForm(credentials, onSave, onCancel) {
    const form = document.createElement('div');
    form.className = 'credentials-form';

    form.innerHTML = `
        <h4>📧 Google Calendar Credentials</h4>
        <p class="help-text">
            Configure your Google Cloud Project OAuth credentials.
            <a href="#" class="help-link" onclick="window.showHelp('sources'); return false;">
                View setup guide
            </a>
        </p>

        <div class="form-group">
            <label for="google-client-id">Client ID *</label>
            <input
                type="text"
                id="google-client-id"
                placeholder="123456789.apps.googleusercontent.com"
                value="${credentials?.client_id || ''}"
                required
            />
            <small>Must end with .apps.googleusercontent.com</small>
        </div>

        <div class="form-group">
            <label for="google-client-secret">Client Secret *</label>
            <input
                type="password"
                id="google-client-secret"
                placeholder="GOCSPX-..."
                value="${credentials?.client_secret || ''}"
                required
            />
            <small>Starts with GOCSPX-</small>
        </div>

        <div class="form-actions">
            <button class="btn btn-primary" id="save-google-creds">Save</button>
            <button class="btn btn-secondary" id="cancel-google-creds">Cancel</button>
        </div>
    `;

    // Event listeners
    form.querySelector('#save-google-creds').addEventListener('click', () => {
        const clientId = form.querySelector('#google-client-id').value.trim();
        const clientSecret = form.querySelector('#google-client-secret').value.trim();

        if (!clientId || !clientSecret) {
            alert('Please fill in all required fields');
            return;
        }

        onSave({ client_id: clientId, client_secret: clientSecret });
    });

    form.querySelector('#cancel-google-creds').addEventListener('click', onCancel);

    return form;
}
