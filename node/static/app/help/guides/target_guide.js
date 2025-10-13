/**
 * Target page guide content.
 */

export const targetGuide = `
<div class="guide-section">
    <h3>🎯 About Target Calendar</h3>
    <p>The target calendar is where all your events from different sources
    will be consolidated. This is the ONE calendar you'll check to see everything.</p>
</div>

<div class="guide-section">
    <h4>How the Target Calendar Works</h4>
    <p>When you sync:</p>
    <ul>
        <li>Events from ALL your source calendars are copied here</li>
        <li>Each event is tagged to show which source it came from</li>
        <li>Updates to source events are reflected in the target</li>
        <li>Deleted source events are removed from the target</li>
    </ul>
    <p class="help-warning">⚠️ <strong>Important:</strong> The target calendar
    will be WRITTEN to. Make sure you choose a calendar you want to use for this purpose.</p>
</div>

<div class="guide-section">
    <h4>Choosing a Target Calendar</h4>
    <p><strong>Best Practice:</strong> Create a new, dedicated calendar for this purpose
    rather than using an existing calendar with important events.</p>
    <p><strong>Why?</strong> Calendar Consolidator manages the target calendar content.
    If you manually add events to the target, they might be affected during sync.</p>
</div>

<div class="guide-section">
    <h4>How to Set Your Target Calendar</h4>
    <ol>
        <li>Click the <strong>"Set Target"</strong> button</li>
        <li>Choose your calendar provider (Microsoft, Google, or iCloud)</li>
        <li>Sign in to your account when prompted</li>
        <li>Grant permission to write to your calendars</li>
        <li>Select the calendar where events should be consolidated</li>
        <li>Click <strong>"Set as Target"</strong> to confirm</li>
    </ol>
    <p class="help-tip">💡 <strong>Tip:</strong> Before setting a target, create a
    new calendar in your provider called "Consolidated Calendar" or similar.</p>
</div>

<div class="guide-section">
    <h4>Understanding Permissions</h4>
    <p>The target calendar requires <strong>write permissions</strong> because the
    app needs to:</p>
    <ul>
        <li>Create new events (from your sources)</li>
        <li>Update existing events (when sources change)</li>
        <li>Delete events (when removed from sources)</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Can I Change the Target?</h4>
    <p>Yes! You can change your target calendar at any time. The previously synced
    events will remain in the old target calendar, and new syncs will use the new target.</p>
</div>

<div class="guide-section">
    <h4>Recommended Setup</h4>
    <p><strong>Example:</strong> If you have Outlook at work and use Google Calendar
    personally, you might:</p>
    <ul>
        <li>Add both Outlook and Google as sources</li>
        <li>Create a new Google Calendar called "All Events"</li>
        <li>Set that new calendar as your target</li>
        <li>View "All Events" on your phone to see everything</li>
    </ul>
</div>
`;
