/**
 * Modal display and management.
 */

import { createHelpPanel } from '../help/index.js';

let helpInitialized = false;

/**
 * Show modal with content.
 */
export function showModal(title, content, onClose = null) {
  const container = document.getElementById('modal-container');

  container.innerHTML = `
    <div class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>${title}</h3>
          <button class="modal-close" onclick="window.closeAddSourceModal()">&times;</button>
        </div>
        <div id="add-source-help-container"></div>
        <div class="modal-body">
          ${content}
        </div>
      </div>
    </div>
  `;

  container.style.display = 'block';

  // Initialize help panel for Add Source modal
  if (!helpInitialized) {
    setTimeout(() => {
      createHelpPanel('add-source', 'add-source-help-container');
      helpInitialized = true;
    }, 100);
  }

  // Store close callback
  if (onClose) {
    window._modalCloseCallback = onClose;
  }
}

/**
 * Update modal body content.
 */
export function updateModalBody(content) {
  const modalBody = document.querySelector('.modal-body');
  if (modalBody) {
    modalBody.innerHTML = content;
  }
}

/**
 * Hide and clear modal.
 */
export function hideModal() {
  const container = document.getElementById('modal-container');
  container.style.display = 'none';
  container.innerHTML = '';

  // Reset help initialization flag
  helpInitialized = false;

  // Call close callback if exists
  if (window._modalCloseCallback) {
    window._modalCloseCallback();
    delete window._modalCloseCallback;
  }
}

/**
 * Show loading state in modal.
 */
export function showLoading(message = 'Loading...') {
  updateModalBody(`
    <div class="loading-container">
      <div class="spinner"></div>
      <p>${message}</p>
    </div>
  `);
}

/**
 * Show error in modal.
 */
export function showError(message) {
  updateModalBody(`
    <div class="error-container">
      <p class="error-message">${message}</p>
      <button class="btn btn-secondary" onclick="window.closeAddSourceModal()">Close</button>
    </div>
  `);
}
