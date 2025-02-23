// src/plugins/vuetify.js
import 'vuetify/styles'          // Global Vuetify styles
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Optionally import an icon font if needed
// import '@mdi/font/css/materialdesignicons.css'

export default createVuetify({
    components,
    directives,
})
