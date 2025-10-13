/**
 * Common OAuth setup content (intro and conclusion).
 */

export const oauthSetupIntro = `
<div class="guide-section">
    <h3>🔑 OAuth Setup (One-Time Configuration)</h3>
    <p>Before you can add calendar sources, you need to set up OAuth credentials
    for each provider. This is a one-time administrative task.</p>
</div>
`;

export const oauthSetupConclusion = `
<div class="guide-section">
    <h4>✅ After Setup</h4>
    <p>Once you have your OAuth credentials:</p>
    <ol>
        <li>Store them securely in the application settings/database</li>
        <li>You can then add as many calendar sources as you want from each provider</li>
        <li>Each source uses the same OAuth app credentials</li>
    </ol>
    <p class="help-tip">💡 <strong>Multiple Accounts:</strong> You can add unlimited
    accounts from each provider - they all share the same OAuth app setup!</p>
</div>
`;
