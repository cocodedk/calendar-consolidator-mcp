/**
 * Add source modal - main orchestration.
 */

import { showModal, hideModal } from './modal.js';
import { showProviderSelector } from './provider_selector.js';
import { startAuthFlow } from './auth_flow.js';
import { showICloudAuthForm } from './icloud_auth_form.js';
import { showCalendarSelector } from './calendar_selector.js';
import { submitCalendars } from './form_handler.js';

/**
 * Show add source modal and start flow.
 */
export async function showAddSourceModal(callbacks = {}) {
  // Show modal with initial state
  showModal('Add Calendar Source', '<div class="loading-container"><div class="spinner"></div></div>');

  // Expose close function globally
  window.closeAddSourceModal = () => {
    hideModal();
    delete window.closeAddSourceModal;
  };

  // Start with provider selection
  showProviderSelector((type) => {
    onProviderSelected(type, callbacks);
  });
}

/**
 * Handle provider selection.
 */
function onProviderSelected(type, callbacks) {
  // iCloud uses form-based auth, others use OAuth
  if (type === 'icloud') {
    showICloudAuthForm((sessionId) => {
      onAuthComplete(sessionId, type, callbacks);
    });
  } else {
    startAuthFlow(type, (sessionId) => {
      onAuthComplete(sessionId, type, callbacks);
    });
  }
}

/**
 * Handle auth completion.
 */
function onAuthComplete(sessionId, type, callbacks) {
  showCalendarSelector(sessionId, type, (sid, t, calendars) => {
    onCalendarsSelected(sid, t, calendars, callbacks);
  });
}

/**
 * Handle calendar selection.
 */
function onCalendarsSelected(sessionId, type, calendars, callbacks) {
  submitCalendars(sessionId, type, calendars, callbacks);
}
