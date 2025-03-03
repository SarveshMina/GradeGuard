// src/services/darkModeService.js

/**
 * Get the saved dark mode preference from localStorage
 * @returns {boolean} True if dark mode is enabled
 */
export function getDarkModePreference() {
    const stored = localStorage.getItem("darkMode");

    // If no preference is set, use system preference
    if (stored === null) {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    return stored === "true";
}

/**
 * Save dark mode preference to localStorage and apply it to the document
 * @param {boolean} isDark - Whether dark mode should be enabled
 */
export function setDarkModePreference(isDark) {
    localStorage.setItem("darkMode", isDark);

    // Apply dark mode class to body
    if (isDark) {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }

    // Dispatch a custom event so other components can react
    window.dispatchEvent(new CustomEvent('darkModeChange', { detail: { isDark } }));
}

/**
 * Initialize dark mode based on stored preference
 * Should be called during app initialization
 */
export function initDarkMode() {
    const isDark = getDarkModePreference();
    setDarkModePreference(isDark);
}

/**
 * Toggle dark mode state
 * @returns {boolean} The new dark mode state
 */
export function toggleDarkMode() {
    const newState = !getDarkModePreference();
    setDarkModePreference(newState);
    return newState;
}