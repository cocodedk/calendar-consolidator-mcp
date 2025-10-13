/**
 * Google Calendar OAuth setup instructions.
 */

export const googleOAuthSetup = `
<div class="guide-section">
    <h4>📧 Google Calendar Setup</h4>
    <p><strong>Step 1: Create Google Cloud Project</strong></p>
    <ol>
        <li>Go to <a href="https://console.cloud.google.com/" target="_blank">Google Cloud Console</a></li>
        <li>Click "Select a project" → "New Project"</li>
        <li>Name it "Calendar Consolidator" and click "Create"</li>
    </ol>

    <p><strong>Step 2: Enable Calendar API</strong></p>
    <ol>
        <li>Navigate to "APIs & Services" → "Library"</li>
        <li>Search for "Google Calendar API"</li>
        <li>Click "Enable"</li>
    </ol>

    <p><strong>Step 3: Configure OAuth Consent Screen</strong></p>
    <ol>
        <li>Go to "APIs & Services" → "OAuth consent screen"</li>
        <li>Select "External" user type</li>
        <li>Fill in: App name, support email, developer contact</li>
        <li>Add scopes: <code>calendar.readonly</code> and <code>calendar.events</code></li>
        <li>Add test users (your email addresses)</li>
    </ol>

    <p><strong>Step 4: Create OAuth Client ID</strong></p>
    <ol>
        <li>Go to "APIs & Services" → "Credentials"</li>
        <li>Click "Create Credentials" → "OAuth client ID"</li>
        <li>Application type: "Desktop app"</li>
        <li>Name: "Calendar Consolidator Desktop"</li>
        <li>Click "Create" and copy the <strong>Client ID</strong> and <strong>Client Secret</strong></li>
    </ol>

    <p class="help-tip">💡 Store these credentials securely - you'll need to configure
    them in the application settings.</p>
</div>
`;
