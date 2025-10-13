/**
 * Help panel localStorage manager.
 */

const STORAGE_PREFIX = 'help-panel-';

export function isHelpExpanded(pageId) {
    const key = `${STORAGE_PREFIX}${pageId}-expanded`;
    const stored = localStorage.getItem(key);
    // Default to expanded for first-time users
    return stored === null ? true : stored === 'true';
}

export function setHelpExpanded(pageId, expanded) {
    const key = `${STORAGE_PREFIX}${pageId}-expanded`;
    localStorage.setItem(key, expanded.toString());
}

export function toggleHelpExpanded(pageId) {
    const current = isHelpExpanded(pageId);
    setHelpExpanded(pageId, !current);
    return !current;
}
