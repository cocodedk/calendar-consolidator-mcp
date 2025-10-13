/**
 * Tab switching functionality.
 */

export function initTabs(loadCallbacks) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName, loadCallbacks);
        });
    });
}

function switchTab(tabName, callbacks) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Load data for tab
    if (tabName === 'dashboard' && callbacks.loadDashboard) callbacks.loadDashboard();
    if (tabName === 'sources' && callbacks.loadSources) callbacks.loadSources();
    if (tabName === 'target' && callbacks.loadTarget) callbacks.loadTarget();
    if (tabName === 'logs' && callbacks.loadLogs) callbacks.loadLogs();
}
