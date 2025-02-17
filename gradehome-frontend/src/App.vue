<!-- App.vue -->
<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { App } from '@capacitor/app'

export default {
  name: 'App',
  setup() {
    const router = useRouter()

    onMounted(() => {
      // Example: Android back button handling
      App.addListener('backButton', () => {
        if (router.currentRoute.value.fullPath !== '/') {
          router.back()
        } else {
          App.exitApp()
        }
      })
    })

    return {}
  },
}
</script>
