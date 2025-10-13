/**
 * Sync page guide content.
 */

export const syncGuide = `
<div class="guide-section">
    <h3>🔄 About Synchronization</h3>
    <p>Synchronization is the process of copying events from your source calendars
    to your target calendar, keeping everything up to date.</p>
</div>

<div class="guide-section">
    <h4>How Sync Works</h4>
    <p>When you run a sync, Calendar Consolidator:</p>
    <ol>
        <li><strong>Reads</strong> all events from your source calendars</li>
        <li><strong>Compares</strong> them with what's in your target calendar</li>
        <li><strong>Creates</strong> new events that don't exist in target yet</li>
        <li><strong>Updates</strong> events that changed in sources</li>
        <li><strong>Deletes</strong> events that were removed from sources</li>
    </ol>
</div>

<div class="guide-section">
    <h4>Preview vs Execute</h4>
    <p><strong>Preview Sync Button:</strong> Shows you what WOULD happen without
    making any changes. This is a safe way to see what will be created, updated,
    or deleted.</p>
    <p><strong>Sync Now Button:</strong> Actually performs the synchronization and
    makes changes to your target calendar.</p>
    <p class="help-tip">💡 <strong>Best Practice:</strong> Always preview first if
    you're unsure! This lets you verify everything looks correct before applying changes.</p>
</div>

<div class="guide-section">
    <h4>Understanding the Preview</h4>
    <p>The preview shows you:</p>
    <ul>
        <li><strong>To Create:</strong> Events that will be added to target calendar</li>
        <li><strong>To Update:</strong> Events that changed and will be updated</li>
        <li><strong>To Delete:</strong> Events that were removed from sources</li>
    </ul>
    <p>You'll see the event title, date/time, and which source it comes from.</p>
</div>

<div class="guide-section">
    <h4>When to Sync</h4>
    <p><strong>Manual Sync:</strong> Click "Sync Now" whenever you want to update
    your target calendar with the latest from your sources.</p>
    <p><strong>Quick Sync:</strong> Use the Quick Sync button on the Dashboard for
    a fast one-click synchronization.</p>
    <p><strong>Automatic Sync:</strong> Enable continuous sync in Settings to
    automatically sync at regular intervals.</p>
</div>

<div class="guide-section">
    <h4>What Gets Synced</h4>
    <p>For each event, we copy:</p>
    <ul>
        <li>Title and description</li>
        <li>Start and end times</li>
        <li>Location</li>
        <li>All-day event status</li>
        <li>Recurrence rules (for repeating events)</li>
    </ul>
</div>

<div class="guide-section">
    <h4>Common Questions</h4>
    <p><strong>How long does sync take?</strong> Usually a few seconds, depending
    on how many events you have.</p>
    <p><strong>What if I delete an event from target?</strong> It will be recreated
    on the next sync if it still exists in a source.</p>
    <p><strong>Can I sync specific sources only?</strong> Not currently - sync
    includes all active sources. You can deactivate sources you don't want to sync.</p>
</div>

<div class="guide-section">
    <p class="help-warning">⚠️ <strong>Note:</strong> Sync requires at least one
    active source and a configured target calendar.</p>
</div>
`;
