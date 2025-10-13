/**
 * Microsoft credentials form component.
 */

export function createMicrosoftCredentialsForm(credentials, onSave, onCancel) {
    const form = document.createElement('div');
    form.className = 'credentials-form';

    form.innerHTML = `
        <h4>📅 Microsoft Outlook/365 Credentials</h4>
        <p class="help-text">
            Configure your Azure AD app registration credentials.
            <a href="#" class="help-link" onclick="window.showHelp('sources'); return false;">
                View setup guide
            </a>
        </p>

        <div class="form-group">
            <label for="ms-client-id">Application (Client) ID *</label>
            <input
                type="text"
                id="ms-client-id"
                placeholder="12345678-1234-1234-1234-123456789012"
                value="${credentials?.client_id || ''}"
                required
            />
            <small>GUID format from Azure portal</small>
        </div>

        <div class="form-group">
            <label for="ms-tenant-id">Directory (Tenant) ID *</label>
            <input
                type="text"
                id="ms-tenant-id"
                placeholder="common or GUID"
                value="${credentials?.tenant_id || 'common'}"
                required
            />
            <small>Use "common" for multi-tenant or your tenant GUID</small>
        </div>

        <div class="form-group">
            <label for="ms-client-secret">Client Secret *</label>
            <input
                type="password"
                id="ms-client-secret"
                placeholder="Your client secret value"
                value="${credentials?.client_secret || ''}"
                required
            />
            <small>From Certificates & secrets in Azure</small>
        </div>

        <div class="form-actions">
            <button class="btn btn-primary" id="save-ms-creds">Save</button>
            <button class="btn btn-secondary" id="cancel-ms-creds">Cancel</button>
        </div>
    `;

    // Event listeners
    form.querySelector('#save-ms-creds').addEventListener('click', () => {
        const clientId = form.querySelector('#ms-client-id').value.trim();
        const tenantId = form.querySelector('#ms-tenant-id').value.trim();
        const clientSecret = form.querySelector('#ms-client-secret').value.trim();

        if (!clientId || !tenantId || !clientSecret) {
            alert('Please fill in all required fields');
            return;
        }

        onSave({
            client_id: clientId,
            tenant_id: tenantId,
            client_secret: clientSecret
        });
    });

    form.querySelector('#cancel-ms-creds').addEventListener('click', onCancel);

    return form;
}
