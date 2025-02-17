// src/plugins/vuetify.js
import 'vuetify/styles'          // Global Vuetify styles
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// If you need Material Design Icons support, also install and import an icon font, e.g.:
// npm install @mdi/font
// import '@mdi/font/css/materialdesignicons.css'

export default createVuetify({
    components,
    directives,
    // theme, icons, etc. can be customized here
})
