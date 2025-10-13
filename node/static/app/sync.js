/**
 * Sync operations functionality.
 */

import { showError } from './utils.js';
import { createHelpPanel } from './help/index.js';

let helpInitialized = false;

function initializeHelp() {
    if (!helpInitialized) {
        createHelpPanel('sync', 'sync-help-container');
        helpInitialized = true;
    }
}

export async function previewSync() {
    initializeHelp();

    try {
        const result = await API.previewSync();
        const container = document.getElementById('sync-preview');

        container.innerHTML = renderPreview(result);
    } catch (error) {
        showError('Preview failed: ' + error.message);
    }
}

function renderPreview(result) {
    return `
        <h3>Preview Results</h3>
        <p>Would create: ${result.wouldCreate} events</p>
        <p>Would update: ${result.wouldUpdate} events</p>
        <p>Would delete: ${result.wouldDelete} events</p>
    `;
}

export async function executeSync(callbacks) {
    initializeHelp();

    if (!confirm('Execute sync now?')) return;

    try {
        const result = await API.executeSync();
        alert(`Sync complete!\nCreated: ${result.created}\nUpdated: ${result.updated}\nDeleted: ${result.deleted}`);
        if (callbacks.loadDashboard) callbacks.loadDashboard();
    } catch (error) {
        showError('Sync failed: ' + error.message);
    }
}

export function quickSync(callbacks) {
    executeSync(callbacks);
}
