<template>
  <div>
    <transition-group
        v-for="position in positions"
        :key="position"
        name="toast"
        tag="div"
        :class="['toast-container', position]"
    >
      <div
          v-for="toast in getToastsByPosition(position)"
          :key="toast.id"
          class="toast-item"
          :class="[toast.type]"
          @click="toast.dismissible && removeToast(toast.id)"
      >
        <div class="toast-content">
          <i v-if="toast.icon" class="toast-icon" :class="toast.icon"></i>
          <div class="toast-message">{{ toast.message }}</div>
          <button
              v-if="toast.dismissible"
              class="toast-close"
              @click.stop="removeToast(toast.id)"
          >
            <i class="fas fa-times"></i> <!-- Changed to FontAwesome -->
          </button>
        </div>

        <div
            v-if="toast.action"
            class="toast-action"
            @click.stop="handleAction(toast)"
        >
          {{ toast.action.text }}
        </div>

        <div class="toast-progress">
          <div
              class="toast-progress-bar"
              :style="{ animationDuration: `${toast.duration}ms` }"
          ></div>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount, onMounted } from 'vue'
import { toastEmitter } from '@/services/toastService.js'

// Supported positions
const positions = [
  'top-right',
  'top-left',
  'bottom-right',
  'bottom-left',
  'top-center',
  'bottom-center'
]

// A reactive array of toasts currently on screen
const toasts = ref([])

// Maximum number of toasts visible at once
const maxToasts = 5

// Group toasts by position
const getToastsByPosition = (position) => {
  return toasts.value.filter(toast => toast.position === position)
}

/**
 * Add a toast to the array, then auto-remove after toast.duration ms.
 */
function addToast(toast) {
  const id = Date.now() + Math.random()
  const position = toast.position || 'top-right'

  // Check if we need to remove old toasts to maintain maximum
  const positionToasts = getToastsByPosition(position)
  if (positionToasts.length >= maxToasts) {
    // Remove the oldest toast in this position
    const oldestId = positionToasts[0].id
    removeToast(oldestId)
  }

  // Add new toast
  toasts.value.push({ ...toast, id, position })

  // Set timeout for auto-dismiss
  if (toast.duration !== Infinity) {
    setTimeout(() => {
      removeToast(id)
    }, toast.duration || 5000) // default 5-second duration
  }
}

/**
 * Remove a toast by id and call its onClose callback if provided
 */
function removeToast(id) {
  const toast = toasts.value.find(t => t.id === id)
  if (toast && typeof toast.onClose === 'function') {
    toast.onClose()
  }
  toasts.value = toasts.value.filter(t => t.id !== id)
}

/**
 * Handle action button click
 */
function handleAction(toast) {
  if (toast.action && typeof toast.action.callback === 'function') {
    toast.action.callback()
  }
  removeToast(toast.id)
}

/**
 * Clear all toasts
 */
function clearAll() {
  toasts.value = []
}

// Listen for events
onMounted(() => {
  toastEmitter.on('notify', addToast)
  toastEmitter.on('clearAll', clearAll)
})

onBeforeUnmount(() => {
  // Remove listeners if this component unmounts
  toastEmitter.off('notify', addToast)
  toastEmitter.off('clearAll', clearAll)
})
</script>

<style scoped>
/* Container that holds all the toasts */
.toast-container {
  position: fixed;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
  max-width: 100%;
  width: 350px;
}

/* Position-specific styles */
.top-right {
  top: 1.5rem;
  right: 1.5rem;
  align-items: flex-end;
}

.top-left {
  top: 1.5rem;
  left: 1.5rem;
  align-items: flex-start;
}

.bottom-right {
  bottom: 1.5rem;
  right: 1.5rem;
  align-items: flex-end;
  flex-direction: column-reverse;
}

.bottom-left {
  bottom: 1.5rem;
  left: 1.5rem;
  align-items: flex-start;
  flex-direction: column-reverse;
}

.top-center {
  top: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  align-items: center;
}

.bottom-center {
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  align-items: center;
  flex-direction: column-reverse;
}

/* Each toast item */
.toast-item {
  pointer-events: auto;
  padding: 0;
  color: #fff;
  border-radius: 8px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  max-width: 100%;
  opacity: 1;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.toast-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 1rem 1rem 0.75rem;
  min-height: 48px;
  gap: 0.75rem;
}

.toast-icon {
  font-size: 1.4rem;
}

.toast-message {
  font-size: 0.95rem;
  line-height: 1.4;
  font-weight: 500;
  flex: 1;
  word-break: break-word;
}

.toast-close {
  background: transparent;
  border: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.7);
  padding: 4px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 1.2rem;
  height: 24px;
  width: 24px;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* Action button */
.toast-action {
  padding: 0.6rem 1rem;
  margin-top: 0rem;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  text-align: right;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.toast-action:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Progress bar */
.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background: rgba(0, 0, 0, 0.15);
}

.toast-progress-bar {
  height: 100%;
  background: rgba(255, 255, 255, 0.4);
  width: 100%;
  transform-origin: left;
  animation: progress-bar linear forwards;
}

@keyframes progress-bar {
  0% {
    transform: scaleX(1);
  }
  100% {
    transform: scaleX(0);
  }
}

/* Enhanced transitions */
.toast-enter-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.6, -0.28, 0.735, 0.045);
}

.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(-15px) scale(0.95);
}

.top-center .toast-enter-from,
.top-center .toast-leave-to,
.bottom-center .toast-enter-from,
.bottom-center .toast-leave-to {
  transform: translateY(-15px) scale(0.95);
}

.bottom-right .toast-enter-from,
.bottom-right .toast-leave-to,
.bottom-left .toast-enter-from,
.bottom-left .toast-leave-to {
  transform: translateY(15px) scale(0.95);
}

/* Toast type styles */
.toast-item.success {
  background-color: #673ab7; /* Purple brand color */
  background-image: linear-gradient(135deg, #673ab7 0%, #512da8 100%);
}

.toast-item.error {
  background-color: #f44336;
  background-image: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
}

.toast-item.info {
  background-color: #2196f3;
  background-image: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
}

.toast-item.warning {
  background-color: #ff9800;
  background-image: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .toast-container {
    width: calc(100% - 2rem);
    padding: 0 1rem;
  }

  .top-right, .top-left, .top-center {
    top: 1rem;
    right: 0;
    left: 0;
    transform: none;
    align-items: stretch;
  }

  .bottom-right, .bottom-left, .bottom-center {
    bottom: 1rem;
    right: 0;
    left: 0;
    transform: none;
    align-items: stretch;
  }
}
</style>