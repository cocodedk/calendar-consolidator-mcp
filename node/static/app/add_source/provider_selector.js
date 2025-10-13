/**
 * Provider selection step.
 */

import { updateModalBody } from './modal.js';

/**
 * Show provider selection UI.
 */
export function showProviderSelector(onSelect) {
  const content = `
    <div class="provider-selector">
      <h4>Select Calendar Provider</h4>
      <p>Choose which calendar service you want to add:</p>

      <div class="provider-options">
        <button class="provider-option" data-type="google">
          <div class="provider-icon">G</div>
          <div class="provider-name">Google Calendar</div>
        </button>

        <button class="provider-option" data-type="graph">
          <div class="provider-icon">M</div>
          <div class="provider-name">Microsoft Outlook</div>
        </button>

        <button class="provider-option" data-type="icloud">
          <div class="provider-icon">🍎</div>
          <div class="provider-name">iCloud Calendar</div>
        </button>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="window.closeAddSourceModal()">Cancel</button>
      </div>
    </div>
  `;

  updateModalBody(content);

  // Attach click handlers
  document.querySelectorAll('.provider-option').forEach(button => {
    button.addEventListener('click', () => {
      const type = button.getAttribute('data-type');
      onSelect(type);
    });
  });
}
