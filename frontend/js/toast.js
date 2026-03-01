/* ============================================
   TOAST NOTIFICATION SYSTEM
   ============================================ */

let containerEl = null;

function ensureContainer() {
    if (!containerEl) {
        containerEl = document.createElement('div');
        containerEl.className = 'toast-container';
        containerEl.id = 'toast-container';
        document.body.appendChild(containerEl);
    }
    return containerEl;
}

/**
 * Show a toast notification.
 * @param {'success'|'error'|'info'} type
 * @param {string} message
 * @param {number} [duration=4000]
 */
export function showToast(type, message, duration = 4000) {
    const container = ensureContainer();

    const icons = {
        success: '✓',
        error: '✕',
        info: 'ℹ',
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
    <span class="toast-icon">${icons[type] || ''}</span>
    <span class="toast-message">${escapeHtml(message)}</span>
  `;

    container.appendChild(toast);

    // Auto-dismiss
    const timer = setTimeout(() => dismiss(toast), duration);

    // Click to dismiss early
    toast.addEventListener('click', () => {
        clearTimeout(timer);
        dismiss(toast);
    });
}

function dismiss(toastEl) {
    toastEl.classList.add('toast-exit');
    toastEl.addEventListener('animationend', () => toastEl.remove());
}

function escapeHtml(str) {
    const el = document.createElement('span');
    el.textContent = str;
    return el.innerHTML;
}
