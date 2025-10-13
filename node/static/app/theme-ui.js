/**
 * Theme UI - Handles theme toggle button and visual updates
 */

/**
 * Update toggle button appearance based on current theme
 */
export function updateToggleButton(theme) {
    const toggleButton = document.getElementById('theme-toggle');
    const themeIcon = toggleButton?.querySelector('.theme-icon');

    if (!themeIcon) return;

    if (theme === 'dark') {
        themeIcon.textContent = '☀️';
        toggleButton.setAttribute('aria-label', 'Switch to light mode');
    } else {
        themeIcon.textContent = '🌙';
        toggleButton.setAttribute('aria-label', 'Switch to dark mode');
    }
}

/**
 * Apply theme to document with optional animation
 */
export function applyThemeToDocument(theme, animate = true) {
    document.documentElement.setAttribute('data-theme', theme);

    if (animate) {
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    updateToggleButton(theme);
}
