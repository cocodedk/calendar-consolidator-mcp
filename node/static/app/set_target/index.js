/**
 * Set target calendar modal flow.
 */

import { showModal, hideModal, showLoading, showError } from '../add_source/modal.js';
import { showProviderSelector } from '../add_source/provider_selector.js';
import { startAuthFlow } from '../add_source/auth_flow.js';
import { showICloudAuthForm } from '../add_source/icloud_auth_form.js';
import { showCalendarSelector } from '../add_source/calendar_selector.js';

/**
 * Show Set Target modal and start flow.
 */
export function showSetTargetModal(callbacks = {}) {
  // Show modal shell
  showModal('Set Target Calendar', '<div class="loading-container"><div class="spinner"></div></div>');

  // Expose close function
  window.closeAddSourceModal = () => {
    hideModal();
    delete window.closeAddSourceModal;
  };

  // Start with provider selection
  showProviderSelector((type) => onProviderSelected(type, callbacks));
}

function onProviderSelected(type, callbacks) {
  // iCloud uses form-based auth, others use OAuth
  if (type === 'icloud') {
    showICloudAuthForm((sessionId) => onAuthComplete(sessionId, type, callbacks));
  } else {
    startAuthFlow(type, (sessionId) => onAuthComplete(sessionId, type, callbacks));
  }
}

function onAuthComplete(sessionId, type, callbacks) {
  // Single calendar selection for target
  showCalendarSelector(sessionId, type, (sid, t, calendars) => {
    onCalendarSelected(sid, t, calendars, callbacks);
  }, { multi: false });
}

async function onCalendarSelected(sessionId, type, calendars, callbacks) {
  if (!calendars || calendars.length !== 1) {
    showError('Please select exactly one calendar.');
    return;
  }

  const selected = calendars[0];
  showLoading('Setting target...');

  try {
    await API.setTarget({
      type,
      calendarId: selected.id,
      name: selected.name,
      sessionId
    });

    hideModal();

    // Refresh UI
    if (callbacks.loadTarget) await callbacks.loadTarget();
    if (callbacks.loadDashboard) await callbacks.loadDashboard();

    alert('Target calendar set successfully.');
  } catch (error) {
    showError('Failed to set target: ' + error.message);
  }
}

