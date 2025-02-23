<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div
          v-for="(toast, index) in toasts"
          :key="toast.id"
          class="toast-item"
          :class="[toast.type]"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { toastEmitter } from '@/services/toastService.js'

// A reactive array of toasts currently on screen
const toasts = ref([])

/**
 * Add a toast to the array, then auto-remove after toast.duration ms.
 */
function addToast(toast) {
  const id = Date.now() + Math.random()
  toasts.value.push({ ...toast, id })

  setTimeout(() => {
    removeToast(id)
  }, toast.duration || 3000) // default 3-second duration
}

/**
 * Remove a toast by id
 */
function removeToast(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// Listen for "notify" events from our toast emitter
toastEmitter.on('notify', addToast)

onBeforeUnmount(() => {
  // Remove the listener if this component unmounts
  toastEmitter.off('notify', addToast)
})
</script>

<style scoped>
/* Container that holds all the toasts */
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Each toast item */
.toast-item {
  padding: 1rem;
  color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  opacity: 0.95;
  max-width: 300px;
  font-weight: 500;
}

/* Basic transition for appear/disappear */
.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Toast type styles */
.toast-item.success {
  background-color: #512da8; /* your purple color */
}
.toast-item.error {
  background-color: #e53935;
}
.toast-item.info {
  background-color: #0288d1;
}
.toast-item.warning {
  background-color: #fbc02d;
}
</style>
