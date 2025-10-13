/**
 * Dashboard functionality.
 */

import { showError } from './utils.js';
import { createHelpPanel } from './help/index.js';

let helpInitialized = false;

export async function loadDashboard() {
    // Initialize help panel once
    if (!helpInitialized) {
        createHelpPanel('dashboard', 'dashboard-help-container');
        helpInitialized = true;
    }

    try {
        const config = await API.getConfig();
        const logs = await API.getLogs(10);

        updateSourcesCount(config);
        updateLastSyncTime(logs);
        updateErrorCount(logs);
    } catch (error) {
        showError('Failed to load dashboard: ' + error.message);
    }
}

function updateSourcesCount(config) {
    const activeCount = config.sources?.filter(s => s.active).length || 0;
    document.getElementById('active-sources-count').textContent = activeCount;
}

function updateLastSyncTime(logs) {
    const lastLog = logs.logs?.[0];
    if (lastLog) {
        document.getElementById('last-sync-time').textContent =
            new Date(lastLog.timestamp).toLocaleString();
    }
}

function updateErrorCount(logs) {
    const errorCount = logs.logs?.filter(l => l.status === 'error').length || 0;
    document.getElementById('error-count').textContent = errorCount;
}
