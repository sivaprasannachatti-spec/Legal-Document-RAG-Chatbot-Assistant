/* ============================================
   APP ENTRY POINT — URL-Based SPA Router
   ============================================ */

import { initLanding, initLogin, initSignup } from './auth.js';
import { initChat } from './chat.js';
import { checkSession } from './api.js';

const rootEl = document.getElementById('app');

// Session state
const SESSION_KEY = 'legalai_user_email';

function getSession() {
    return localStorage.getItem(SESSION_KEY);
}
function setSession(email) {
    localStorage.setItem(SESSION_KEY, email);
}
function clearSession() {
    localStorage.removeItem(SESSION_KEY);
}

/**
 * Navigate to a page using the browser URL.
 * @param {'/'|'/login'|'/signup'|'/chat'} path
 * @param {string} [data] - optional data (e.g. prefill email)
 */
function navigate(path, data) {
    // Normalize path names from old function calls
    const pathMap = {
        'landing': '/',
        'login': '/login',
        'signup': '/signup',
        'chat': '/chat',
    };
    const resolved = pathMap[path] || path;

    // Push to browser history
    if (window.location.pathname !== resolved) {
        history.pushState({ data }, '', resolved);
    }

    renderPage(resolved, data);
}

/**
 * Render the correct page based on URL path.
 */
function renderPage(path, data) {
    document.body.style.overflow = path === '/chat' ? 'hidden' : 'auto';

    const onAuthSuccess = (email) => {
        setSession(email);
        navigate('/chat');
    };

    switch (path) {
        case '/login':
            initLogin(rootEl, navigate, onAuthSuccess);
            break;

        case '/signup':
            initSignup(rootEl, navigate, onAuthSuccess, data || '');
            break;

        case '/chat': {
            const email = getSession();
            if (!email) {
                navigate('/login');
                return;
            }
            initChat(rootEl, email, () => {
                clearSession();
                navigate('/');
            });
            break;
        }

        case '/':
        default:
            initLanding(rootEl, navigate);
            break;
    }
}

// Handle browser back/forward buttons
window.addEventListener('popstate', (e) => {
    const data = e.state?.data || '';
    renderPage(window.location.pathname, data);
});

// Boot — check if user is already authenticated via cookie
async function boot() {
    const path = window.location.pathname;

    try {
        // Try to verify the JWT cookie with the backend
        const data = await checkSession();
        if (data.authenticated && data.email) {
            // User is already logged in — save email and go to chat
            setSession(data.email);
            if (path === '/' || path === '/login' || path === '/signup') {
                navigate('/chat');
            } else {
                renderPage(path);
            }
            return;
        }
    } catch (err) {
        // Cookie is missing or expired — clear local session
        clearSession();
    }

    // Not authenticated — render the requested page
    // (login/signup pages will show, /chat will redirect to /login)
    renderPage(path);
}

boot();
