/**
 * Theme Manager - Main theme management module
 */

import { getInitialTheme, saveTheme, getSavedTheme } from './theme-storage.js';
import { applyThemeToDocument } from './theme-ui.js';

class ThemeManager {
    constructor() {
        this.currentTheme = getInitialTheme();

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    init() {
        const toggleButton = document.getElementById('theme-toggle');

        if (!toggleButton) {
            console.error('Theme toggle button not found');
            return;
        }

        applyThemeToDocument(this.currentTheme, false);

        toggleButton.addEventListener('click', () => this.toggle());

        window.matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', (e) => this.handleSystemChange(e));
    }

    toggle() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        applyThemeToDocument(this.currentTheme);
        saveTheme(this.currentTheme);
    }

    handleSystemChange(event) {
        if (!getSavedTheme()) {
            this.currentTheme = event.matches ? 'dark' : 'light';
            applyThemeToDocument(this.currentTheme);
        }
    }

    getCurrentTheme() {
        return this.currentTheme;
    }
}

const themeManager = new ThemeManager();
export default themeManager;
