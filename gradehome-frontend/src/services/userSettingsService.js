// src/services/userSettingsService.js
import axios from 'axios';
import { notify } from '@/services/toastService.js';
import { setDarkModePreference } from '@/services/darkModeService.js';
import { API_URL } from '@/config.js';

export const userSettingsService = {
    // Fetch user settings from the server
    async fetchSettings() {
        try {
            const response = await axios.get(`${API_URL}/user/settings`, {
                withCredentials: true,
            });

            if (response.data) {
                return response.data;
            }
            return null;
        } catch (error) {
            console.error("Error fetching user settings:", error);
            // If 404, it means settings haven't been created yet
            if (error.response?.status === 404) {
                return this.getDefaultSettings();
            }
            return null;
        }
    },

    // Get user settings from localStorage (synchronous)
    getUserSettings() {
        const settingsJson = localStorage.getItem('userSettings');
        if (settingsJson) {
            try {
                return JSON.parse(settingsJson);
            } catch (e) {
                console.error("Error parsing user settings from localStorage:", e);
                return null;
            }
        }
        return null;
    },

    // Get settings (for backward compatibility)
    getSettings() {
        return this.getUserSettings();
    },

    // Apply settings to the app
    applySettings(settings) {
        if (!settings) return;

        // Apply dark mode
        if (settings.appearance) {
            const isDarkMode = !!settings.appearance.darkMode;
            setDarkModePreference(isDarkMode);

            // Dispatch the event for other components
            window.dispatchEvent(new CustomEvent('darkModeChange', {
                detail: { isDark: isDarkMode }
            }));

            // Apply accent color
            if (settings.appearance.accentColor) {
                this.applyAccentColor(settings.appearance.accentColor);
            }

            // Apply font size
            if (settings.appearance.fontSize) {
                this.applyFontSize(settings.appearance.fontSize);
            }

            // Apply high contrast if enabled
            if (settings.appearance.highContrast) {
                document.documentElement.classList.add('high-contrast');
            } else {
                document.documentElement.classList.remove('high-contrast');
            }
        }

        // Apply keyboard shortcuts
        if (settings.accessibility) {
            localStorage.setItem('keyboardShortcuts',
                settings.accessibility.keyboardShortcuts ? 'true' : 'false');

            // Dispatch event for App.vue
            window.dispatchEvent(new CustomEvent('settingsChange', {
                detail: {
                    setting: 'keyboardShortcuts',
                    value: settings.accessibility.keyboardShortcuts
                }
            }));

            // Apply focus mode if enabled
            if (settings.accessibility.focusMode) {
                document.documentElement.classList.add('focus-mode');
            } else {
                document.documentElement.classList.remove('focus-mode');
            }
        }

        // Save settings to localStorage for quick access
        localStorage.setItem('userSettings', JSON.stringify(settings));
    },

    // Helper to apply accent color
    applyAccentColor(colorId) {
        const colorMap = {
            'purple': '#7b49ff',
            'blue': '#2196f3',
            'green': '#4caf50',
            'red': '#f44336',
            'orange': '#ff9800',
            'pink': '#e91e63',
            'teal': '#009688'
        };

        const color = colorMap[colorId] || colorMap['purple'];
        document.documentElement.style.setProperty('--primary-color', color);

        // Calculate darker variant for hover states
        const darkerColor = this.adjustColor(color, -20);
        document.documentElement.style.setProperty('--primary-dark', darkerColor);

        // Calculate lighter variant
        const lighterColor = this.adjustColor(color, 20);
        document.documentElement.style.setProperty('--primary-light', lighterColor);
    },

    // Helper to apply font size
    applyFontSize(size) {
        const sizeMap = {
            'small': '14px',
            'medium': '16px',
            'large': '18px'
        };

        document.documentElement.style.setProperty('--font-size-base', sizeMap[size] || '16px');
    },

    // Helper to adjust color brightness
    adjustColor(hex, amount) {
        // Convert hex to RGB
        let r = parseInt(hex.slice(1, 3), 16);
        let g = parseInt(hex.slice(3, 5), 16);
        let b = parseInt(hex.slice(5, 7), 16);

        // Adjust colors
        r = Math.max(0, Math.min(255, r + amount));
        g = Math.max(0, Math.min(255, g + amount));
        b = Math.max(0, Math.min(255, b + amount));

        // Convert back to hex
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    },

    // Default settings
    getDefaultSettings() {
        return {
            appearance: {
                accentColor: 'purple',
                fontSize: 'medium',
                highContrast: false,
                darkMode: false
            },
            academic: {
                gradingScale: [
                    { letter: 'A', minPercentage: 90, gpaValue: 4.0 },
                    { letter: 'B', minPercentage: 80, gpaValue: 3.0 },
                    { letter: 'C', minPercentage: 70, gpaValue: 2.0 },
                    { letter: 'D', minPercentage: 60, gpaValue: 1.0 },
                    { letter: 'F', minPercentage: 0, gpaValue: 0.0 }
                ],
                termStartDate: '',
                termEndDate: '',
                holidays: []
            },
            accessibility: {
                screenReaderOptimized: false,
                keyboardShortcuts: true,
                focusMode: false
            },
            calendar: {
                firstDayOfWeek: 'sunday',
                defaultEventDuration: '60',
                defaultEventType: 'general',
                timeFormat: '12h',
                dateFormat: 'MM/DD/YYYY'
            }
        };
    }
};