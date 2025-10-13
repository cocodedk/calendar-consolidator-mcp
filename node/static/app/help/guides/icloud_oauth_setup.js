/**
 * iCloud Calendar OAuth setup instructions.
 */

export const icloudOAuthSetup = `
<div class="guide-section">
    <h4>🍎 iCloud Calendar Setup</h4>
    <p><strong>Step 1: Enable Two-Factor Authentication</strong></p>
    <ol>
        <li>Go to <a href="https://appleid.apple.com/" target="_blank">Apple ID Account</a></li>
        <li>Sign in with your Apple ID</li>
        <li>Navigate to "Sign-In and Security"</li>
        <li>Enable Two-Factor Authentication if not already enabled</li>
    </ol>

    <p><strong>Step 2: Generate App-Specific Password</strong></p>
    <ol>
        <li>In "Sign-In and Security", select "App-Specific Passwords"</li>
        <li>Click "+" or "Generate an app-specific password"</li>
        <li>Enter label: "Calendar Consolidator"</li>
        <li>Click "Create"</li>
        <li>Copy the password (format: xxxx-xxxx-xxxx-xxxx)</li>
    </ol>

    <p class="help-warning">⚠️ <strong>Save it now:</strong> You won't be able to see
    this password again!</p>

    <p class="help-tip">💡 <strong>Note:</strong> For iCloud, you'll need to generate
    a separate app-specific password for each iCloud account you want to add.</p>
</div>
`;
