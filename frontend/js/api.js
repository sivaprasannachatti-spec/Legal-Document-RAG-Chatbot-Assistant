/* ============================================
   API SERVICE — All backend HTTP calls
   ============================================ */

const API_BASE = '/api';

/**
 * Generic fetch wrapper with JSON parsing, cookie auth, and error handling.
 */
async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    credentials: 'include',  // send cookies (access_token)
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const message = data?.detail || data?.message || `Request failed (${response.status})`;
      throw { status: response.status, message };
    }

    return data;
  } catch (err) {
    if (err.status) throw err;  // already formatted
    throw { status: 0, message: 'Network error — please check your connection.' };
  }
}

/* ---------- Auth ---------- */

export async function signup(name, email) {
  return apiFetch('/user/signup', {
    method: 'POST',
    body: JSON.stringify({ name, email }),
  });
}

export async function login(email) {
  return apiFetch('/user/login', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
}

export async function logout() {
  return apiFetch('/user/logout', {
    method: 'DELETE',
  });
}

export async function getUserDetails(email) {
  return apiFetch(`/user/details/${encodeURIComponent(email)}`);
}

export async function checkSession() {
  return apiFetch('/user/me');
}

/* ---------- Chat ---------- */

export async function getAllChats() {
  return apiFetch('/chat/getAllChats');
}

export async function getParticularChat(chatTitle) {
  return apiFetch(`/chat/getParticularChat/${encodeURIComponent(chatTitle)}`);
}

export async function sendNewChat(message) {
  return apiFetch('/chat/newChat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}

export async function sendOldChat(chatTitle, message) {
  return apiFetch(`/chat/oldChat/${encodeURIComponent(chatTitle)}`, {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}
