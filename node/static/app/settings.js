/**
 * Settings functionality.
 */

import { createHelpPanel } from './help/index.js';
import { createCredentialsSection } from './settings/credentials_section.js';

let helpInitialized = false;
let credentialsInitialized = false;

export async function loadSettings() {
    // Initialize help panel once
    if (!helpInitialized) {
        createHelpPanel('settings', 'settings-help-container');
        helpInitialized = true;
    }

    // Initialize credentials section once
    if (!credentialsInitialized) {
        const container = document.getElementById('settings-content');
        if (container) {
            const section = await createCredentialsSection();
            container.appendChild(section);
            credentialsInitialized = true;
        }
    }
}
