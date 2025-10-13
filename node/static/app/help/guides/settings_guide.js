/**
 * Settings page guide content.
 */

export const settingsGuide = `
<div class="guide-section">
    <h3>⚙️ About Settings</h3>
    <p>Settings let you customize how Calendar Consolidator works and control
    automatic synchronization behavior.</p>
</div>

<div class="guide-section">
    <h4>Enable Continuous Sync</h4>
    <p>When enabled, Calendar Consolidator will automatically sync your calendars
    at regular intervals without you needing to click "Sync Now".</p>
    <p><strong>How it works:</strong></p>
    <ul>
        <li>Sync runs automatically in the background</li>
        <li>Your target calendar stays up to date</li>
        <li>You'll see the latest events without manual intervention</li>
    </ul>
    <p><strong>When to use it:</strong> Enable this if you want your consolidated
    calendar to always show the latest information without having to remember to sync.</p>
    <p><strong>When to disable it:</strong> Disable if you prefer manual control,
    or if you have API rate limits to consider.</p>
</div>

<div class="guide-section">
    <h4>Sync Interval (Minutes)</h4>
    <p>This controls how often automatic sync runs when continuous sync is enabled.</p>
    <p><strong>Available range:</strong> 1 to 60 minutes</p>
    <p><strong>Recommendations:</strong></p>
    <ul>
        <li><strong>5 minutes:</strong> Good for busy schedules with frequent changes</li>
        <li><strong>15 minutes:</strong> Balanced for most users</li>
        <li><strong>30-60 minutes:</strong> If your calendar doesn't change often</li>
    </ul>
    <p class="help-warning">⚠️ <strong>Note:</strong> More frequent syncing means
    more API calls to calendar services. Some providers have rate limits.</p>
</div>

<div class="guide-section">
    <h4>Ignore Private Events</h4>
    <p>When enabled, events marked as "private" or "confidential" in your source
    calendars will NOT be copied to the target calendar.</p>
    <p><strong>Why use this?</strong></p>
    <ul>
        <li>Keep sensitive meetings private</li>
        <li>Share your target calendar with others while hiding personal events</li>
        <li>Maintain privacy for confidential work meetings</li>
    </ul>
    <p><strong>What happens:</strong> Private events are completely skipped during
    sync. They won't appear in preview or logs either.</p>
    <p class="help-tip">💡 <strong>Tip:</strong> Even with this disabled, Calendar
    Consolidator respects the privacy flags - the events are copied but remain
    marked as private.</p>
</div>

<div class="guide-section">
    <h4>Saving Your Settings</h4>
    <p>After making changes, click <strong>"Save Settings"</strong> to apply them.
    Settings take effect immediately:</p>
    <ul>
        <li>Continuous sync will start/stop based on your choice</li>
        <li>New interval will be used for the next automatic sync</li>
        <li>Privacy settings apply to the next sync operation</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Recommended Configuration</h4>
    <p><strong>For personal use:</strong></p>
    <ul>
        <li>Enable continuous sync</li>
        <li>Set interval to 15 minutes</li>
        <li>Keep private events if it's just for you</li>
    </ul>
    <p><strong>For shared calendars:</strong></p>
    <ul>
        <li>Enable continuous sync</li>
        <li>Set interval to 30 minutes</li>
        <li>Enable "Ignore Private Events" to protect privacy</li>
    </ul>
    <p><strong>For manual control:</strong></p>
    <ul>
        <li>Disable continuous sync</li>
        <li>Use Quick Sync or Sync Now when you need it</li>
    </ul>
</div>
`;
