// src/services/darkModeService.js

export function getDarkModePreference() {
    // default is 'false' if not set
    const stored = localStorage.getItem('darkMode')
    return stored === 'true'
}

export function setDarkModePreference(isDark) {
    localStorage.setItem('darkMode', isDark)
}
