// src/services/toastService.js

import mitt from 'mitt'

// A shared event bus for toast notifications
export const toastEmitter = mitt()

/**
 * Send a toast notification.
 * @param {Object} options
 * @param {('success'|'error'|'info'|'warning')} options.type - Type of toast.
 * @param {string} options.message - The message to display.
 * @param {number} options.duration - How long (ms) before it auto-hides. Defaults to 5000.
 * @param {string} options.icon - Custom icon (uses any icon set). If not provided, a default icon based on type will be used.
 * @param {boolean} options.dismissible - Whether the toast can be closed manually. Defaults to true.
 * @param {string} options.position - Position of the toast ('top-right', 'top-left', 'bottom-right', 'bottom-left', 'top-center', 'bottom-center'). Defaults to 'top-right'.
 * @param {Function} options.onClose - Callback when toast is closed.
 * @param {Object} options.action - Optional action button { text: string, callback: Function }
 */
export function notify({
                           type = 'success',
                           message = '',
                           duration = 5000,
                           icon = '',
                           dismissible = true,
                           position = 'top-right',
                           onClose = null,
                           action = null
                       }) {
    // Provide default icons based on type if no custom icon is specified
    if (!icon) {
        switch (type) {
            case 'success':
                icon = 'fas fa-check-circle' // Using FontAwesome instead of MDI
                break
            case 'error':
                icon = 'fas fa-exclamation-circle'
                break
            case 'info':
                icon = 'fas fa-info-circle'
                break
            case 'warning':
                icon = 'fas fa-exclamation-triangle'
                break
            default:
                icon = 'fas fa-bell'
        }
    }

    toastEmitter.emit('notify', {
        type,
        message,
        duration,
        icon,
        dismissible,
        position,
        onClose,
        action,
        timestamp: Date.now()
    })
}

/**
 * Shorthand methods for different toast types
 */
notify.success = (message, options = {}) => notify({ type: 'success', message, ...options })
notify.error = (message, options = {}) => notify({ type: 'error', message, ...options })
notify.info = (message, options = {}) => notify({ type: 'info', message, ...options })
notify.warning = (message, options = {}) => notify({ type: 'warning', message, ...options })

/**
 * Clear all active toasts
 */
notify.clearAll = () => {
    toastEmitter.emit('clearAll')
}