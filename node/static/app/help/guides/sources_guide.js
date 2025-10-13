/**
 * Sources page guide content.
 */

import { oauthSetupIntro, oauthSetupConclusion } from './oauth_setup_common.js';
import { googleOAuthSetup } from './google_oauth_setup.js';
import { microsoftOAuthSetup } from './microsoft_oauth_setup.js';
import { icloudOAuthSetup } from './icloud_oauth_setup.js';

export const sourcesGuide = `
<div class="guide-section">
    <h3>📚 About Source Calendars</h3>
    <p>Sources are the calendars you want to sync FROM. Think of them as the
    calendars that contain events you want to see in your consolidated view.</p>
</div>

<div class="guide-section">
    <h4>⚙️ First-Time Setup Required</h4>
    <p class="help-warning">⚠️ <strong>Before Adding Sources:</strong> You must configure
    OAuth credentials for each calendar provider you want to use. This is a one-time setup.</p>
    <p>See the <strong>"OAuth Setup"</strong> section below for detailed instructions for
    Google, Microsoft, and iCloud.</p>
</div>

<div class="guide-section">
    <h4>How Source Calendars Work</h4>
    <p>When you add a source calendar:</p>
    <ul>
        <li>Calendar Consolidator connects to that calendar service</li>
        <li>It reads events from those calendars (read-only access)</li>
        <li>Events are copied to your target calendar during sync</li>
        <li>Your original calendars remain completely unchanged</li>
    </ul>
    <p class="help-tip">💡 <strong>Safe & Secure:</strong> We only READ from source
    calendars. Your original events are never modified or deleted.</p>
</div>

<div class="guide-section">
    <h4>How to Add a Source Calendar</h4>
    <ol>
        <li>Click the <strong>"+ Add Source"</strong> button</li>
        <li>Choose your calendar provider (Microsoft, Google, or iCloud)</li>
        <li>Sign in to your account when prompted</li>
        <li>Grant permission to read your calendars</li>
        <li>Select which specific calendars you want to sync</li>
        <li>Click <strong>"Add Source"</strong> to finish</li>
    </ol>
</div>

<div class="guide-section">
    <h4>Supported Calendar Providers</h4>
    <ul>
        <li><strong>Microsoft 365 / Outlook:</strong> Personal, work, or school accounts</li>
        <li><strong>Google Calendar:</strong> Gmail and Google Workspace accounts</li>
        <li><strong>iCloud Calendar:</strong> Apple ID calendars</li>
    </ul>
    <p class="help-tip">💡 <strong>Tip:</strong> You can add multiple sources from the
    same provider! For example, add both your work and personal Google calendars.</p>
</div>

<div class="guide-section">
    <h4>Managing Your Sources</h4>
    <p><strong>Active Status:</strong> Shows whether a source is currently being synced.
    Inactive sources won't be included in synchronization.</p>
    <p><strong>Removing a Source:</strong> Click the "Remove" button to stop syncing
    from a calendar. Events already copied to your target calendar will remain there.</p>
</div>

<div class="guide-section">
    <h4>Common Scenarios</h4>
    <p><strong>Multiple Work Calendars:</strong> Add your main calendar, team calendar,
    and shared project calendars as separate sources.</p>
    <p><strong>Work + Personal:</strong> Combine your work Outlook with personal Google
    Calendar to see everything in one place.</p>
    <p><strong>Family Calendars:</strong> Add calendars from multiple family members
    to coordinate schedules.</p>
</div>

${oauthSetupIntro}
${googleOAuthSetup}
${microsoftOAuthSetup}
${icloudOAuthSetup}
${oauthSetupConclusion}
`;
