/**
 * Logs display functionality.
 */

import { showError } from './utils.js';

export async function loadLogs() {
    try {
        const result = await API.getLogs();
        const container = document.getElementById('logs-list');

        if (!result.logs || result.logs.length === 0) {
            container.innerHTML = '<p>No logs yet.</p>';
            return;
        }

        container.innerHTML = result.logs.map(renderLog).join('');
    } catch (error) {
        showError('Failed to load logs: ' + error.message);
    }
}

function renderLog(log) {
    const errorHtml = log.error_message
        ? `<br><span style="color: red;">${log.error_message}</span>`
        : '';

    return `
        <div class="log-entry ${log.status}">
            <strong>${new Date(log.timestamp).toLocaleString()}</strong> - ${log.status}
            <br>Created: ${log.created_count}, Updated: ${log.updated_count}, Deleted: ${log.deleted_count}
            ${errorHtml}
        </div>
    `;
}
