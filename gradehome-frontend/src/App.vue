<template>
  <v-app>
    <!-- Our toast manager sits on top, so it can show notifications any time -->
    <ToastManager />
    <router-view />
  </v-app>
</template>

<script>
import ToastManager from '@/components/ToastManager.vue'

export default {
  name: 'App',
  components: {
    ToastManager
  }
}
</script>
