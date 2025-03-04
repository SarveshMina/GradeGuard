// src/plugins/vuetify.js
import 'vuetify/styles'          // Global Vuetify styles
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Material Design Icons import commented out - requires installation
// import '@mdi/font/css/materialdesignicons.css'

// Define custom theme matching GradeGuard colors
export default createVuetify({
    components,
    directives,
    // Set default icons to use vuetify's built-in set
    icons: {
        defaultSet: 'mdi',
    },
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                dark: false,
                colors: {
                    primary: '#673ab7',     // Main purple color
                    secondary: '#9c27b0',   // Secondary purple
                    accent: '#4caf50',      // Success green
                    error: '#f44336',       // Error red
                    warning: '#ff9800',     // Warning orange
                    info: '#2196f3',        // Info blue
                    success: '#4caf50'      // Success green
                }
            },
            dark: {
                dark: true,
                colors: {
                    primary: '#9575cd',     // Lighter purple for dark theme
                    secondary: '#ce93d8',   // Lighter secondary for dark theme
                    accent: '#81c784',      // Lighter green for dark theme
                    error: '#e57373',       // Lighter red for dark theme
                    warning: '#ffb74d',     // Lighter orange for dark theme
                    info: '#64b5f6',        // Lighter blue for dark theme
                    success: '#81c784'      // Lighter green for dark theme
                }
            }
        }
    }
})