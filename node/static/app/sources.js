/**
 * Sources management functionality.
 */

import { showError } from './utils.js';
import { createHelpPanel } from './help/index.js';

let helpInitialized = false;

export async function loadSources() {
    // Initialize help panel once
    if (!helpInitialized) {
        createHelpPanel('sources', 'sources-help-container');
        helpInitialized = true;
    }

    try {
        const config = await API.getConfig();
        const container = document.getElementById('sources-list');

        if (!config.sources || config.sources.length === 0) {
            container.innerHTML = '<p>No sources configured. Add one to get started.</p>';
            return;
        }

        container.innerHTML = config.sources.map(renderSource).join('');
    } catch (error) {
        showError('Failed to load sources: ' + error.message);
    }
}

function renderSource(source) {
    return `
        <div class="card">
            <h3>${source.name || source.calendar_id}</h3>
            <p>Type: ${source.type}</p>
            <p>Status: ${source.active ? 'Active' : 'Inactive'}</p>
            <button class="btn" onclick="window.removeSource(${source.id})">Remove</button>
        </div>
    `;
}

export async function removeSource(sourceId, callbacks) {
    if (!confirm('Remove this source?')) return;

    try {
        await API.removeSource(sourceId);
        if (callbacks.loadSources) callbacks.loadSources();
        if (callbacks.loadDashboard) callbacks.loadDashboard();
    } catch (error) {
        showError('Failed to remove source: ' + error.message);
    }
}

export async function showAddSource(callbacks = {}) {
    const { showAddSourceModal } = await import('./add_source/index.js');
    showAddSourceModal(callbacks);
}
