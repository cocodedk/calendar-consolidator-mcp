/**
 * Calendar selection step.
 */

import { updateModalBody, showError, showLoading } from './modal.js';

/**
 * Fetch and display available calendars.
 */
export async function showCalendarSelector(sessionId, type, onSubmit) {
  showLoading('Loading calendars...');

  try {
    const response = await fetch(`/api/auth/calendars/${sessionId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to load calendars');
    }

    const { calendars } = await response.json();

    displayCalendarList(calendars, sessionId, type, onSubmit);

  } catch (error) {
    showError(`Error loading calendars: ${error.message}`);
  }
}

/**
 * Display calendar list with checkboxes.
 */
function displayCalendarList(calendars, sessionId, type, onSubmit) {
  const calendarItems = calendars.map((cal, index) => `
    <label class="calendar-item">
      <input type="checkbox" name="calendar" value="${index}" data-id="${cal.id}" data-name="${cal.name}">
      <span class="calendar-name">${cal.name}</span>
      ${cal.canWrite ? '<span class="badge">Read/Write</span>' : '<span class="badge badge-readonly">Read Only</span>'}
    </label>
  `).join('');

  const content = `
    <div class="calendar-selector">
      <h4>Select Calendars</h4>
      <p>Choose one or more calendars to add as sources:</p>

      <div class="calendar-list">
        ${calendarItems}
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="window.closeAddSourceModal()">Cancel</button>
        <button class="btn btn-primary" id="submit-calendars">Add Selected</button>
      </div>
    </div>
  `;

  updateModalBody(content);

  // Attach submit handler
  document.getElementById('submit-calendars').addEventListener('click', () => {
    const selectedCheckboxes = document.querySelectorAll('input[name="calendar"]:checked');

    if (selectedCheckboxes.length === 0) {
      alert('Please select at least one calendar');
      return;
    }

    const selectedCalendars = Array.from(selectedCheckboxes).map(checkbox => ({
      id: checkbox.getAttribute('data-id'),
      name: checkbox.getAttribute('data-name')
    }));

    onSubmit(sessionId, type, selectedCalendars);
  });
}
