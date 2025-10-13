/**
 * Core help panel UI component.
 */

import { isHelpExpanded, toggleHelpExpanded } from './help_storage.js';
import { getGuideContent } from './help_content.js';

export function createHelpPanel(pageId, containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container ${containerId} not found`);
        return;
    }

    const content = getGuideContent(pageId);
    if (!content) {
        console.error(`No guide content for page: ${pageId}`);
        return;
    }

    const expanded = isHelpExpanded(pageId);
    const panelId = `help-panel-${pageId}`;

    const panel = document.createElement('div');
    panel.className = 'help-panel';
    panel.id = panelId;

    panel.innerHTML = `
        <button class="help-toggle" aria-label="Toggle help" aria-expanded="${expanded}">
            <span class="help-icon">?</span>
            <span class="help-label">Help</span>
        </button>
        <div class="help-content ${expanded ? 'expanded' : 'collapsed'}">
            ${content}
        </div>
    `;

    // Insert at the beginning of the container
    container.insertBefore(panel, container.firstChild);

    // Add toggle functionality
    const toggleBtn = panel.querySelector('.help-toggle');
    const contentDiv = panel.querySelector('.help-content');

    toggleBtn.addEventListener('click', () => {
        const newExpanded = toggleHelpExpanded(pageId);
        toggleBtn.setAttribute('aria-expanded', newExpanded);
        contentDiv.classList.toggle('expanded', newExpanded);
        contentDiv.classList.toggle('collapsed', !newExpanded);
    });
}
