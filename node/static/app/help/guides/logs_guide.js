/**
 * Logs page guide content.
 */

export const logsGuide = `
<div class="guide-section">
    <h3>📋 About Sync Logs</h3>
    <p>Logs show you a history of all synchronization operations, helping you
    track what happened and troubleshoot any issues.</p>
</div>

<div class="guide-section">
    <h4>What Information Do Logs Show?</h4>
    <p>Each log entry includes:</p>
    <ul>
        <li><strong>Timestamp:</strong> When the sync ran</li>
        <li><strong>Status:</strong> Whether it succeeded or failed</li>
        <li><strong>Details:</strong> What was created, updated, or deleted</li>
        <li><strong>Errors:</strong> Any problems that occurred (if applicable)</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Understanding Log Statuses</h4>
    <p><strong>✓ Success:</strong> Sync completed without problems. All events
    were processed correctly.</p>
    <p><strong>⚠️ Warning:</strong> Sync completed but some events had issues.
    Check the details to see what was skipped.</p>
    <p><strong>✗ Error:</strong> Sync failed to complete. Check the error message
    to understand what went wrong.</p>
</div>

<div class="guide-section">
    <h4>Reading Log Details</h4>
    <p>Successful sync logs show:</p>
    <ul>
        <li>Number of events created</li>
        <li>Number of events updated</li>
        <li>Number of events deleted</li>
        <li>Which sources were included</li>
        <li>Total time taken</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Troubleshooting with Logs</h4>
    <p><strong>No events synced?</strong> Check if your sources have any events
    in the date range you're syncing.</p>
    <p><strong>Authentication errors?</strong> Your credentials may have expired.
    Try removing and re-adding the affected source or target.</p>
    <p><strong>Permission errors?</strong> The calendar service may have revoked
    access. Re-authorize the connection.</p>
    <p><strong>Rate limit errors?</strong> You may be syncing too frequently.
    Wait a few minutes and try again.</p>
</div>

<div class="guide-section">
    <h4>Common Error Messages</h4>
    <p><strong>"No target configured":</strong> You need to set a target calendar
    in the Target tab before syncing.</p>
    <p><strong>"No active sources":</strong> Add at least one source calendar in
    the Sources tab.</p>
    <p><strong>"Authentication failed":</strong> Your login credentials need to
    be refreshed. Re-add the calendar connection.</p>
    <p><strong>"Calendar not found":</strong> The calendar may have been deleted
    or permissions changed. Check in the calendar provider.</p>
</div>

<div class="guide-section">
    <h4>Refreshing Logs</h4>
    <p>Click the <strong>"Refresh"</strong> button to load the latest log entries.
    This is useful right after running a sync to see the results.</p>
    <p class="help-tip">💡 <strong>Tip:</strong> Logs are automatically saved for
    your last 100 sync operations, so you can always look back at history.</p>
</div>

<div class="guide-section">
    <h4>When to Check Logs</h4>
    <ul>
        <li>After running a sync to confirm it worked</li>
        <li>If events aren't appearing as expected</li>
        <li>To see how many events are being synced regularly</li>
        <li>When troubleshooting connection problems</li>
    </ul>
</div>
`;
