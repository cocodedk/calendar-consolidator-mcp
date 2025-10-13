/**
 * Target calendar functionality.
 */

import { showError } from './utils.js';
import { createHelpPanel } from './help/index.js';

let helpInitialized = false;

export async function loadTarget() {
    // Initialize help panel once
    if (!helpInitialized) {
        createHelpPanel('target', 'target-help-container');
        helpInitialized = true;
    }

    try {
        const config = await API.getConfig();
        const container = document.getElementById('target-info');

        if (!config.target) {
            container.innerHTML = '<p>No target configured. Set one to enable syncing.</p>';
            return;
        }

        container.innerHTML = renderTarget(config.target);
    } catch (error) {
        showError('Failed to load target: ' + error.message);
    }
}

function renderTarget(target) {
    return `
        <h3>${target.name || target.calendar_id}</h3>
        <p>Type: ${target.type}</p>
    `;
}

export function showSetTarget() {
    alert('Set target functionality - integrate OAuth flow here');
}
