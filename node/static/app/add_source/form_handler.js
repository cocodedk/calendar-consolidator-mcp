/**
 * Form submission handler.
 */

import { showLoading, showError, hideModal } from './modal.js';

/**
 * Submit selected calendars to create sources.
 */
export async function submitCalendars(sessionId, type, calendars, callbacks) {
  showLoading('Adding calendars...');

  try {
    // Get session to retrieve credentials
    const sessionResponse = await fetch(`/api/auth/poll/${sessionId}`);

    if (!sessionResponse.ok) {
      throw new Error('Failed to retrieve session');
    }

    // Fetch credentials from session via a new endpoint or pass sessionId
    // For now, we'll add each calendar by making individual API calls
    const results = [];

    for (const calendar of calendars) {
      try {
        const response = await fetch('/api/source', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type,
            calendarId: calendar.id,
            name: calendar.name,
            sessionId // Pass sessionId so backend can retrieve credentials
          })
        });

        if (!response.ok) {
          const error = await response.json();
          results.push({ calendar: calendar.name, success: false, error: error.error });
        } else {
          const data = await response.json();
          results.push({ calendar: calendar.name, success: true, sourceId: data.sourceId });
        }
      } catch (error) {
        results.push({ calendar: calendar.name, success: false, error: error.message });
      }
    }

    // Check if any succeeded
    const successCount = results.filter(r => r.success).length;

    if (successCount === 0) {
      showError('Failed to add any calendars. Please try again.');
      return;
    }

    // Close modal and refresh sources list
    hideModal();

    if (callbacks && callbacks.loadSources) {
      await callbacks.loadSources();
    }

    // Show success message
    const message = successCount === calendars.length
      ? `Successfully added ${successCount} calendar(s)!`
      : `Added ${successCount} of ${calendars.length} calendar(s). Some failed.`;

    alert(message);

  } catch (error) {
    showError(`Error adding calendars: ${error.message}`);
  }
}
