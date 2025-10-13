/**
 * Settings functionality.
 */

import { createHelpPanel } from './help/index.js';

let helpInitialized = false;

export function loadSettings() {
    // Initialize help panel once
    if (!helpInitialized) {
        createHelpPanel('settings', 'settings-help-container');
        helpInitialized = true;
    }
}
