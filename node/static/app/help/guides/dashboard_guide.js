/**
 * Dashboard page guide content.
 */

export const dashboardGuide = `
<div class="guide-section">
    <h3>📊 Welcome to Calendar Consolidator</h3>
    <p>This dashboard shows you an overview of your calendar synchronization system at a glance.</p>
</div>

<div class="guide-section">
    <h4>What is Calendar Consolidator?</h4>
    <p>Calendar Consolidator helps you combine multiple calendars from different services
    (like Microsoft Outlook, Google Calendar, and iCloud) into one unified calendar.
    Instead of checking multiple places, all your events appear in a single target calendar.</p>
</div>

<div class="guide-section">
    <h4>Understanding the Dashboard</h4>
    <ul>
        <li><strong>Active Sources:</strong> How many calendars you're syncing FROM</li>
        <li><strong>Last Sync:</strong> When your calendars were last synchronized</li>
        <li><strong>Recent Errors:</strong> Any problems that occurred during recent syncs</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Quick Sync Button</h4>
    <p>Click this button to immediately sync all your calendars. This will:</p>
    <ol>
        <li>Check all your source calendars for new or changed events</li>
        <li>Copy those events to your target calendar</li>
        <li>Remove events that were deleted from sources</li>
    </ol>
    <p class="help-tip">💡 <strong>Tip:</strong> Use Quick Sync after making changes to
    see them reflected immediately!</p>
</div>

<div class="guide-section">
    <h4>Getting Started</h4>
    <ol>
        <li>Go to the <strong>Sources</strong> tab to add calendars you want to sync from</li>
        <li>Go to the <strong>Target</strong> tab to set where events should be copied to</li>
        <li>Return here and click <strong>Quick Sync</strong> to sync everything</li>
    </ol>
</div>

<div class="guide-section">
    <p class="help-warning">⚠️ <strong>Note:</strong> You need at least one source and
    one target calendar before you can sync.</p>
</div>
`;
