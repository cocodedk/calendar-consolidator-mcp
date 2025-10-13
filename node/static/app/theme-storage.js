/**
 * Theme Storage - Handles localStorage operations for theme persistence
 */

const STORAGE_KEY = 'theme';

/**
 * Get saved theme from localStorage
 */
export function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY);
}

/**
 * Save theme to localStorage
 */
export function saveTheme(theme) {
    localStorage.setItem(STORAGE_KEY, theme);
}

/**
 * Check system color scheme preference
 */
export function getSystemPreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * Get initial theme (saved or system preference)
 */
export function getInitialTheme() {
    const savedTheme = getSavedTheme();
    return savedTheme || getSystemPreference();
}
