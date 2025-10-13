/**
 * Main application logic.
 * Handles UI interactions and updates.
 */

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Load data for tab
    if (tabName === 'dashboard') loadDashboard();
    if (tabName === 'sources') loadSources();
    if (tabName === 'target') loadTarget();
    if (tabName === 'logs') loadLogs();
}

// Dashboard
async function loadDashboard() {
    try {
        const config = await API.getConfig();
        const logs = await API.getLogs(10);

        document.getElementById('active-sources-count').textContent =
            config.sources?.filter(s => s.active).length || 0;

        const lastLog = logs.logs?.[0];
        if (lastLog) {
            document.getElementById('last-sync-time').textContent =
                new Date(lastLog.timestamp).toLocaleString();
        }

        const errorCount = logs.logs?.filter(l => l.status === 'error').length || 0;
        document.getElementById('error-count').textContent = errorCount;
    } catch (error) {
        showError('Failed to load dashboard: ' + error.message);
    }
}

// Sources
async function loadSources() {
    try {
        const config = await API.getConfig();
        const container = document.getElementById('sources-list');

        if (!config.sources || config.sources.length === 0) {
            container.innerHTML = '<p>No sources configured. Add one to get started.</p>';
            return;
        }

        container.innerHTML = config.sources.map(source => `
            <div class="card">
                <h3>${source.name || source.calendar_id}</h3>
                <p>Type: ${source.type}</p>
                <p>Status: ${source.active ? 'Active' : 'Inactive'}</p>
                <button class="btn" onclick="removeSource(${source.id})">Remove</button>
            </div>
        `).join('');
    } catch (error) {
        showError('Failed to load sources: ' + error.message);
    }
}

// Target
async function loadTarget() {
    try {
        const config = await API.getConfig();
        const container = document.getElementById('target-info');

        if (!config.target) {
            container.innerHTML = '<p>No target configured. Set one to enable syncing.</p>';
            return;
        }

        container.innerHTML = `
            <h3>${config.target.name || config.target.calendar_id}</h3>
            <p>Type: ${config.target.type}</p>
        `;
    } catch (error) {
        showError('Failed to load target: ' + error.message);
    }
}

// Sync operations
async function previewSync() {
    try {
        const result = await API.previewSync();
        const container = document.getElementById('sync-preview');

        container.innerHTML = `
            <h3>Preview Results</h3>
            <p>Would create: ${result.wouldCreate} events</p>
            <p>Would update: ${result.wouldUpdate} events</p>
            <p>Would delete: ${result.wouldDelete} events</p>
        `;
    } catch (error) {
        showError('Preview failed: ' + error.message);
    }
}

async function executeSync() {
    if (!confirm('Execute sync now?')) return;

    try {
        const result = await API.executeSync();
        alert(`Sync complete!\nCreated: ${result.created}\nUpdated: ${result.updated}\nDeleted: ${result.deleted}`);
        loadDashboard();
    } catch (error) {
        showError('Sync failed: ' + error.message);
    }
}

async function quickSync() {
    executeSync();
}

// Logs
async function loadLogs() {
    try {
        const result = await API.getLogs();
        const container = document.getElementById('logs-list');

        if (!result.logs || result.logs.length === 0) {
            container.innerHTML = '<p>No logs yet.</p>';
            return;
        }

        container.innerHTML = result.logs.map(log => `
            <div class="log-entry ${log.status}">
                <strong>${new Date(log.timestamp).toLocaleString()}</strong> - ${log.status}
                <br>Created: ${log.created_count}, Updated: ${log.updated_count}, Deleted: ${log.deleted_count}
                ${log.error_message ? `<br><span style="color: red;">${log.error_message}</span>` : ''}
            </div>
        `).join('');
    } catch (error) {
        showError('Failed to load logs: ' + error.message);
    }
}

// Utility functions
function showError(message) {
    alert('Error: ' + message);
}

function showAddSource() {
    alert('Add source functionality - integrate OAuth flow here');
}

function showSetTarget() {
    alert('Set target functionality - integrate OAuth flow here');
}

async function removeSource(sourceId) {
    if (!confirm('Remove this source?')) return;

    try {
        await API.removeSource(sourceId);
        loadSources();
        loadDashboard();
    } catch (error) {
        showError('Failed to remove source: ' + error.message);
    }
}

// Initialize
loadDashboard();
