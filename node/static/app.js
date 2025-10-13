/**
 * Main application - re-export and initialize from modular structure.
 */

import { initTabs } from './app/tabs.js';
import { loadDashboard } from './app/dashboard.js';
import { loadSources, removeSource, showAddSource } from './app/sources.js';
import { loadTarget, showSetTarget } from './app/target.js';
import { previewSync, executeSync, quickSync } from './app/sync.js';
import { loadLogs } from './app/logs.js';
import { loadSettings } from './app/settings.js';

// Create callbacks object
const callbacks = {
    loadDashboard,
    loadSources,
    loadTarget,
    loadLogs,
    loadSettings
};

// Initialize tabs
initTabs(callbacks);

// Expose global functions for onclick handlers
window.removeSource = (sourceId) => removeSource(sourceId, callbacks);
window.showAddSource = () => showAddSource(callbacks);
window.showSetTarget = showSetTarget;
window.previewSync = previewSync;
window.executeSync = () => executeSync(callbacks);
window.quickSync = () => quickSync(callbacks);

// Initialize dashboard
loadDashboard();
