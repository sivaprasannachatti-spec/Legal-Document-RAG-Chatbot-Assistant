/* ============================================
   CHAT MODULE — Chat UI logic
   ============================================ */

import { getAllChats, getParticularChat, sendNewChat, sendOldChat, logout } from './api.js';
import { showToast } from './toast.js';

let currentChatTitle = null;
let chatList = [];          // [{title, messages}]
let userEmail = '';
let userName = '';
let sidebarOpen = true;

/**
 * Initialize the chat page.
 * @param {HTMLElement} rootEl
 * @param {string} email
 * @param {Function} onLogout - called when user logs out
 */
export function initChat(rootEl, email, onLogout) {
  userEmail = email;
  userName = email.split('@')[0];
  currentChatTitle = null;
  chatList = [];
  render(rootEl);
  bindEvents(rootEl, onLogout);
  loadChats(rootEl);
}

/* ============================================
   RENDERING
   ============================================ */

function render(rootEl) {
  rootEl.innerHTML = `
    <div class="app-shell" id="app-shell">
      <!-- ======== SIDEBAR ======== -->
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
          <div class="sidebar-logo">
            <div class="sidebar-logo-icon">⚖️</div>
            <div class="sidebar-logo-name">Legal<span>AI</span></div>
          </div>
          <button class="btn btn-icon btn-ghost" id="sidebar-close-btn" title="Close sidebar">✕</button>
        </div>

        <div class="sidebar-new-chat">
          <button class="btn btn-primary" id="new-chat-btn">
            <span>＋</span>
            New Chat
          </button>
        </div>

        <div class="sidebar-chats" id="sidebar-chat-list">
          <div class="sidebar-section-title">Your Conversations</div>
          <!-- Chat items rendered dynamically -->
          <div id="chat-list-items"></div>
        </div>

        <div class="sidebar-footer">
          <div class="sidebar-user">
            <div class="avatar avatar-user" id="user-avatar">${getInitials(userName)}</div>
            <div class="sidebar-user-info">
              <div class="sidebar-user-name" id="sidebar-user-name">${escapeHtml(userName)}</div>
              <div class="sidebar-user-email" id="sidebar-user-email">${escapeHtml(userEmail)}</div>
            </div>
            <div class="sidebar-user-actions">
              <button class="btn btn-icon btn-ghost" id="logout-btn" title="Logout">⏻</button>
            </div>
          </div>
        </div>
      </aside>

      <!-- ======== MAIN ======== -->
      <div class="main-content" id="main-content">
        <!-- Header -->
        <header class="main-header">
          <button class="btn btn-icon btn-ghost main-header-toggle" id="sidebar-toggle-btn" title="Toggle sidebar">☰</button>
          <h2 class="main-header-title" id="main-header-title">New Chat</h2>
          <div class="main-header-badge badge">
            <span class="status-dot"></span>
            <span>Online</span>
          </div>
        </header>

        <!-- Chat messages -->
        <div class="chat-area" id="chat-area">
          <div class="chat-messages" id="chat-messages">
            ${renderWelcome()}
          </div>
        </div>

        <!-- Input -->
        <div class="chat-input-area">
          <div class="chat-input-wrapper" id="chat-input-wrapper">
            <textarea id="chat-input" rows="1" placeholder="Ask about legal documents, contracts, clauses…"></textarea>
            <button class="chat-send-btn" id="chat-send-btn" title="Send message" disabled>➤</button>
          </div>
          <div class="chat-input-hint">LegalAI can make mistakes. Review important legal information carefully.</div>
        </div>
      </div>
    </div>
  `;
}

function renderWelcome() {
  return `
    <div class="chat-welcome" id="chat-welcome">
      <div class="chat-welcome-icon">⚖️</div>
      <h2>Legal Document Assistant</h2>
      <p>Ask me anything about legal contracts, clauses, agreements, and regulatory documents. I'll search through the document corpus to give you accurate, sourced answers.</p>
      <div class="chat-suggestions">
        <button class="suggestion-card" data-suggestion="What are the key terms in a joint venture agreement?">
          <div class="suggestion-card-title">Joint Ventures</div>
          Key terms and obligations
        </button>
        <button class="suggestion-card" data-suggestion="Explain the termination clause in a distributor agreement">
          <div class="suggestion-card-title">Termination Clauses</div>
          Distributor agreement analysis
        </button>
        <button class="suggestion-card" data-suggestion="What is a co-branding agreement and what does it typically include?">
          <div class="suggestion-card-title">Co-Branding</div>
          Agreement structure overview
        </button>
        <button class="suggestion-card" data-suggestion="Summarize the key obligations in a services agreement">
          <div class="suggestion-card-title">Service Agreements</div>
          Obligations & liabilities
        </button>
      </div>
    </div>
  `;
}

function renderMessage(role, content) {
  const isUser = role === 'user';
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return `
    <div class="message ${isUser ? 'message-user' : 'message-ai'}">
      <div class="avatar ${isUser ? 'avatar-user' : 'avatar-ai'}">
        ${isUser ? getInitials(userName) : '⚖️'}
      </div>
      <div class="message-content">
        <div class="message-header">
          <span class="message-sender">${isUser ? 'You' : 'LegalAI'}</span>
          <span class="message-time">${time}</span>
        </div>
        <div class="message-body">
          ${formatMessageBody(content)}
        </div>
      </div>
    </div>
  `;
}

function renderTypingIndicator() {
  return `
    <div class="message message-ai" id="typing-indicator">
      <div class="avatar avatar-ai">⚖️</div>
      <div class="message-content">
        <div class="message-header">
          <span class="message-sender">LegalAI</span>
        </div>
        <div class="message-body" style="padding: 0;">
          <div class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderChatListItems() {
  const container = document.getElementById('chat-list-items');
  if (!container) return;

  if (chatList.length === 0) {
    container.innerHTML = `
      <div style="padding: var(--space-6) var(--space-4); text-align: center; color: var(--color-text-muted); font-size: var(--text-sm);">
        No conversations yet.<br/>Start a new chat!
      </div>
    `;
    return;
  }

  container.innerHTML = chatList.map(chat => `
    <div class="chat-item ${chat.title === currentChatTitle ? 'active' : ''}" data-chat-title="${escapeAttr(chat.title)}">
      <span class="chat-item-icon">💬</span>
      <span class="chat-item-title">${escapeHtml(chat.title)}</span>
    </div>
  `).join('');
}

/* ============================================
   EVENTS
   ============================================ */

function bindEvents(rootEl, onLogout) {
  // Sidebar toggle
  const sidebarEl = rootEl.querySelector('#sidebar');
  const sidebarCloseBtn = rootEl.querySelector('#sidebar-close-btn');
  const sidebarToggle = rootEl.querySelector('#sidebar-toggle-btn');

  sidebarCloseBtn.addEventListener('click', () => toggleSidebar(sidebarEl));
  sidebarToggle.addEventListener('click', () => toggleSidebar(sidebarEl));

  // New chat
  rootEl.querySelector('#new-chat-btn').addEventListener('click', () => startNewChat(rootEl));

  // Send message
  const input = rootEl.querySelector('#chat-input');
  const sendBtn = rootEl.querySelector('#chat-send-btn');

  input.addEventListener('input', () => {
    sendBtn.disabled = !input.value.trim();
    autoResize(input);
  });
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.value.trim()) handleSend(rootEl);
    }
  });
  sendBtn.addEventListener('click', () => handleSend(rootEl));

  // Suggestion cards
  rootEl.addEventListener('click', (e) => {
    const card = e.target.closest('.suggestion-card');
    if (card) {
      input.value = card.dataset.suggestion;
      sendBtn.disabled = false;
      handleSend(rootEl);
    }
  });

  // Chat list clicks
  rootEl.addEventListener('click', (e) => {
    const item = e.target.closest('.chat-item');
    if (item) {
      const title = item.dataset.chatTitle;
      openChat(rootEl, title);
    }
  });

  // Logout
  rootEl.querySelector('#logout-btn').addEventListener('click', async () => {
    try {
      await logout();
      showToast('success', 'Logged out successfully');
      onLogout();
    } catch (err) {
      showToast('error', err.message || 'Logout failed');
    }
  });
}

/* ============================================
   ACTIONS
   ============================================ */

function toggleSidebar(sidebarEl) {
  sidebarOpen = !sidebarOpen;
  sidebarEl.classList.toggle('collapsed', !sidebarOpen);
}

function startNewChat(rootEl) {
  currentChatTitle = null;
  const messagesEl = rootEl.querySelector('#chat-messages');
  const headerTitle = rootEl.querySelector('#main-header-title');
  messagesEl.innerHTML = renderWelcome();
  headerTitle.textContent = 'New Chat';
  renderChatListItems();
}

async function openChat(rootEl, title) {
  currentChatTitle = title;
  const messagesEl = rootEl.querySelector('#chat-messages');
  const headerTitle = rootEl.querySelector('#main-header-title');
  headerTitle.textContent = title;

  // Show loading
  messagesEl.innerHTML = `
    <div style="display: flex; justify-content: center; padding: var(--space-10);">
      <div class="spinner spinner-lg"></div>
    </div>
  `;

  renderChatListItems();

  try {
    const data = await getParticularChat(title);
    const messages = data.chat?.chat_id || [];

    messagesEl.innerHTML = messages.map(m =>
      renderMessage(m.role === 'LLM' ? 'ai' : 'user', m.content)
    ).join('');

    scrollToBottom(rootEl);
  } catch (err) {
    messagesEl.innerHTML = renderWelcome();
    showToast('error', err.message || 'Failed to load chat');
  }
}

async function handleSend(rootEl) {
  const input = rootEl.querySelector('#chat-input');
  const sendBtn = rootEl.querySelector('#chat-send-btn');
  const messagesEl = rootEl.querySelector('#chat-messages');
  const headerTitle = rootEl.querySelector('#main-header-title');
  const message = input.value.trim();

  if (!message) return;

  // Clear welcome screen if visible
  const welcome = rootEl.querySelector('#chat-welcome');
  if (welcome) welcome.remove();

  // Add user message
  messagesEl.insertAdjacentHTML('beforeend', renderMessage('user', message));
  input.value = '';
  sendBtn.disabled = true;
  autoResize(input);
  scrollToBottom(rootEl);

  // Show typing indicator
  messagesEl.insertAdjacentHTML('beforeend', renderTypingIndicator());
  scrollToBottom(rootEl);

  try {
    let data;
    if (currentChatTitle) {
      // Continue existing chat
      data = await sendOldChat(currentChatTitle, message);
      const aiResponse = data.LLM_response || data.response || '';
      removeTypingIndicator();
      messagesEl.insertAdjacentHTML('beforeend', renderMessage('ai', aiResponse));
    } else {
      // New chat
      data = await sendNewChat(message);
      const aiResponse = data.response || '';
      removeTypingIndicator();
      messagesEl.insertAdjacentHTML('beforeend', renderMessage('ai', aiResponse));

      // Refresh chat list to pick up the new chat title
      await loadChats(rootEl);

      // Set current chat title from the response
      // We reload and pick the first new chat
      if (chatList.length > 0) {
        const newTitle = chatList[chatList.length - 1]?.title || 'New Chat';
        currentChatTitle = newTitle;
        headerTitle.textContent = newTitle;
        renderChatListItems();
      }
    }

    scrollToBottom(rootEl);
  } catch (err) {
    removeTypingIndicator();
    showToast('error', err.message || 'Failed to send message');
  }
}

async function loadChats(rootEl) {
  try {
    const data = await getAllChats();
    const titles = data.chats || [];

    chatList = titles.map(title => ({
      title,
      messages: [],
    }));

    renderChatListItems();
  } catch (err) {
    console.warn('Failed to load chats:', err.message);
    chatList = [];
    renderChatListItems();
  }
}

/* ============================================
   HELPERS
   ============================================ */

function scrollToBottom(rootEl) {
  const area = rootEl.querySelector('#chat-area');
  if (area) {
    requestAnimationFrame(() => {
      area.scrollTop = area.scrollHeight;
    });
  }
}

function removeTypingIndicator() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
}

function getInitials(name) {
  return name.charAt(0).toUpperCase();
}

function escapeHtml(str) {
  const el = document.createElement('span');
  el.textContent = str;
  return el.innerHTML;
}

function escapeAttr(str) {
  return str.replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function formatMessageBody(content) {
  if (!content) return '<p></p>';
  // Simple markdown-like: paragraphs, bold, code
  return content
    .split('\n\n')
    .filter(Boolean)
    .map(para => {
      let html = escapeHtml(para);
      // Bold: **text**
      html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // Inline code: `text`
      html = html.replace(/`(.*?)`/g, '<code style="background:var(--color-surface);padding:2px 6px;border-radius:4px;font-size:0.875em;">$1</code>');
      // Line breaks
      html = html.replace(/\n/g, '<br>');
      return `<p>${html}</p>`;
    })
    .join('');
}
