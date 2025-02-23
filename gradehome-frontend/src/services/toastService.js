// src/services/toastService.js

import mitt from 'mitt'

// A shared event bus for toast notifications
export const toastEmitter = mitt()

/**
 * Send a toast notification.
 * @param {Object} options
 * @param {('success'|'error'|'info'|'warning')} options.type - Type of toast.
 * @param {string} options.message - The message to display.
 * @param {number} options.duration - How long (ms) before it auto-hides. Defaults to 3000.
 */
export function notify({ type = 'success', message = '', duration = 3000 }) {
    toastEmitter.emit('notify', { type, message, duration })
}
