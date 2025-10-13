/**
 * Microsoft Outlook/365 OAuth setup instructions.
 */

export const microsoftOAuthSetup = `
<div class="guide-section">
    <h4>📅 Microsoft Outlook/365 Setup</h4>
    <p><strong>Step 1: Register Application in Azure</strong></p>
    <ol>
        <li>Go to <a href="https://portal.azure.com/" target="_blank">Azure Portal</a></li>
        <li>Navigate to "Azure Active Directory" → "App registrations"</li>
        <li>Click "New registration"</li>
        <li>Name: "Calendar Consolidator"</li>
        <li>Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"</li>
        <li>Redirect URI: Leave blank for now (device code flow)</li>
        <li>Click "Register"</li>
    </ol>

    <p><strong>Step 2: Note Your IDs</strong></p>
    <ol>
        <li>On the app overview page, copy the <strong>Application (client) ID</strong></li>
        <li>Copy the <strong>Directory (tenant) ID</strong></li>
    </ol>

    <p><strong>Step 3: Create Client Secret</strong></p>
    <ol>
        <li>Go to "Certificates & secrets" → "Client secrets"</li>
        <li>Click "New client secret"</li>
        <li>Add description: "Calendar Consolidator Secret"</li>
        <li>Choose expiration (24 months recommended)</li>
        <li>Click "Add" and copy the <strong>Client Secret Value</strong> immediately</li>
    </ol>

    <p><strong>Step 4: Configure API Permissions</strong></p>
    <ol>
        <li>Go to "API permissions"</li>
        <li>Click "Add a permission" → "Microsoft Graph"</li>
        <li>Select "Delegated permissions"</li>
        <li>Add: <code>Calendars.ReadWrite</code> and <code>Calendars.Read</code></li>
        <li>Click "Add permissions"</li>
    </ol>

    <p class="help-warning">⚠️ <strong>Important:</strong> Copy the Client Secret immediately -
    you won't be able to see it again!</p>
</div>
`;
