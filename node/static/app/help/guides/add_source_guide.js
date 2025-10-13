/**
 * Add Source modal guide content.
 */

export const addSourceGuide = `
<div class="guide-section">
    <h3>➕ Adding a Source Calendar</h3>
    <p>This wizard will help you connect a calendar from Microsoft, Google,
    or iCloud to use as a source.</p>
</div>

<div class="guide-section">
    <h4>Step 1: Choose Your Provider</h4>
    <p>Select which calendar service you want to connect:</p>
    <ul>
        <li><strong>Microsoft:</strong> Outlook, Office 365, or work/school accounts</li>
        <li><strong>Google:</strong> Gmail or Google Workspace calendars</li>
        <li><strong>iCloud:</strong> Apple Calendar with your Apple ID</li>
    </ul>
    <p class="help-tip">💡 <strong>Don't see your provider?</strong> Currently,
    these are the only supported services, but more may be added in the future.</p>
</div>

<div class="guide-section">
    <h4>Step 2: Sign In and Authorize</h4>
    <p>You'll be asked to sign in to your calendar service:</p>
    <ol>
        <li>A sign-in window or form will appear</li>
        <li>Enter your username/email and password</li>
        <li>You may need to complete two-factor authentication</li>
        <li>Review and accept the permission request</li>
    </ol>
    <p><strong>What permissions are needed?</strong> Calendar Consolidator needs
    permission to READ your calendars. We never write to or modify source calendars.</p>
    <p class="help-warning">⚠️ <strong>Security:</strong> Your credentials are
    handled directly by the calendar provider (Microsoft, Google, Apple). Calendar
    Consolidator never sees your password.</p>
</div>

<div class="guide-section">
    <h4>Step 3: Select Calendars</h4>
    <p>After signing in, you'll see a list of all calendars in your account:</p>
    <ul>
        <li>Check the box next to each calendar you want to sync</li>
        <li>You can select multiple calendars from the same account</li>
        <li>Uncheck any you don't want to include</li>
    </ul>
    <p class="help-tip">💡 <strong>Tip:</strong> You can always add more calendars
    from the same account later by going through this process again.</p>
</div>

<div class="guide-section">
    <h4>Step 4: Finish Adding Source</h4>
    <p>Click <strong>"Add Source"</strong> to complete the setup. Your selected
    calendars will:</p>
    <ul>
        <li>Appear in the Sources list</li>
        <li>Be marked as Active by default</li>
        <li>Be included in the next sync operation</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Troubleshooting Sign-In Issues</h4>
    <p><strong>Can't sign in?</strong> Make sure you're using the correct username
    and password. For work accounts, you may need to use your full email address.</p>
    <p><strong>Two-factor required?</strong> Complete the 2FA process on your phone
    or authenticator app as normal.</p>
    <p><strong>iCloud issues?</strong> You may need to generate an app-specific
    password in your Apple ID settings if you have 2FA enabled.</p>
    <p><strong>Permission denied?</strong> Make sure you click "Allow" or "Accept"
    when asked to grant calendar access.</p>
</div>

<div class="guide-section">
    <h4>After Adding a Source</h4>
    <p>Once added:</p>
    <ul>
        <li>The source will appear in your Sources list</li>
        <li>Run a sync to see its events in your target calendar</li>
        <li>You can add more sources following the same process</li>
        <li>To remove a source later, use the "Remove" button in Sources</li>
    </ul>
</div>
`;
