/* ============================================
   AUTH MODULE — Login / Signup / Landing
   ============================================ */

import { login, signup } from './api.js';
import { showToast } from './toast.js';

/* ---- Shared Navbar ---- */
function renderNavbar(activePage) {
  return `
    <nav class="navbar" id="navbar">
      <a class="navbar-brand" id="nav-home">
        <div class="navbar-brand-icon">⚖️</div>
        <div class="navbar-brand-text">Legal<span>AI</span></div>
      </a>
      <div class="navbar-links">
        <a class="navbar-link ${activePage === 'chat' ? 'active' : ''}" id="nav-chat">
          💬 <span class="link-label">Chat</span>
        </a>
        <a class="navbar-link ${activePage === 'login' ? 'active' : ''}" id="nav-login">
          🔑 <span class="link-label">Login</span>
        </a>
        <button class="navbar-btn-signup ${activePage === 'signup' ? 'active' : ''}" id="nav-signup">
          Sign Up
        </button>
      </div>
    </nav>
  `;
}

function bindNavbar(rootEl, navigate) {
  rootEl.querySelector('#nav-home')?.addEventListener('click', (e) => { e.preventDefault(); navigate('/'); });
  rootEl.querySelector('#nav-chat')?.addEventListener('click', (e) => { e.preventDefault(); navigate('/login'); showToast('info', 'Please log in to access chat'); });
  rootEl.querySelector('#nav-login')?.addEventListener('click', (e) => { e.preventDefault(); navigate('/login'); });
  rootEl.querySelector('#nav-signup')?.addEventListener('click', () => navigate('/signup'));
}

/* ============================================
   LANDING PAGE
   ============================================ */

export function initLanding(rootEl, navigate) {
  rootEl.innerHTML = `
    ${renderNavbar('landing')}
    <div class="landing-page">
      <!-- Background glows -->
      <div class="landing-bg-glow"></div>
      <div class="landing-bg-glow"></div>

      <div class="landing-content">
        <!-- Hero -->
        <section class="hero">
          <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            AI-Powered Legal Research
          </div>
          <h1>
            Your Intelligent<br/>
            <span class="gradient-text">Legal Document Assistant</span>
          </h1>
          <p class="hero-description">
            Ask questions about contracts, clauses, and agreements. Get accurate, sourced answers powered by advanced RAG technology and your legal document corpus.
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary btn-lg" id="hero-get-started">
              Get Started Free →
            </button>
            <button class="btn btn-outline btn-lg" id="hero-login">
              Sign In
            </button>
          </div>
        </section>

        <!-- Features -->
        <section class="features-section">
          <h2 class="features-title">Powerful Features</h2>
          <p class="features-subtitle">Everything you need for legal document analysis</p>
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">🔍</div>
              <h3 class="feature-title">Smart Search</h3>
              <p class="feature-description">AI-powered retrieval across your entire legal document corpus with semantic understanding.</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">💬</div>
              <h3 class="feature-title">Natural Conversations</h3>
              <p class="feature-description">Ask questions in plain English and receive detailed, sourced answers from your documents.</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">📄</div>
              <h3 class="feature-title">Document Analysis</h3>
              <p class="feature-description">Analyze contracts, agreements, and clauses with precision. Understand obligations and risks.</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">🔒</div>
              <h3 class="feature-title">Secure & Private</h3>
              <p class="feature-description">Your documents and conversations are encrypted and stored securely. Your data stays yours.</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">📚</div>
              <h3 class="feature-title">Chat History</h3>
              <p class="feature-description">All your research conversations are saved. Pick up right where you left off anytime.</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">⚡</div>
              <h3 class="feature-title">Instant Answers</h3>
              <p class="feature-description">Get responses in seconds, not hours. Speed up your legal research workflow dramatically.</p>
            </div>
          </div>
        </section>

        <!-- Stats -->
        <section class="stats-section">
          <div class="stats-bar">
            <div class="stat-item">
              <div class="stat-value">5+</div>
              <div class="stat-label">Legal Documents</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">RAG</div>
              <div class="stat-label">Powered Retrieval</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">24/7</div>
              <div class="stat-label">Available</div>
            </div>
          </div>
        </section>

        <!-- Footer -->
        <footer class="landing-footer">
          <p>© 2026 LegalAI. Built with FastAPI, LangChain & FAISS. All rights reserved.</p>
        </footer>
      </div>
    </div>
  `;

  bindNavbar(rootEl, navigate);

  // Hero buttons
  rootEl.querySelector('#hero-get-started').addEventListener('click', () => navigate('/signup'));
  rootEl.querySelector('#hero-login').addEventListener('click', () => navigate('/login'));
}

/* ============================================
   LOGIN PAGE
   ============================================ */

export function initLogin(rootEl, navigate, onAuthSuccess) {
  rootEl.innerHTML = `
    ${renderNavbar('login')}
    <div class="auth-page" id="auth-page">
      <div class="auth-bg-orb"></div>
      <div class="auth-bg-orb"></div>
      <div class="auth-bg-orb"></div>

      <div class="auth-card glass-panel">
        <div class="auth-logo">
          <div class="auth-logo-icon">⚖️</div>
          <div class="auth-logo-text">Legal<span>AI</span></div>
        </div>

        <h1 class="modal-title">Welcome back</h1>
        <p class="modal-subtitle">Sign in to continue with your legal assistant</p>

        <form class="auth-form-container" id="login-form" autocomplete="off">
          <div class="input-group">
            <label for="login-email">Email Address</label>
            <input class="input" type="email" id="login-email" placeholder="you@example.com" maxlength="100" required />
          </div>

          <button type="submit" class="btn btn-primary btn-lg" id="login-submit-btn">
            <span id="login-submit-text">Sign In</span>
            <div class="spinner" id="login-spinner" style="display: none;"></div>
          </button>
        </form>

        <div class="auth-footer">
          Don't have an account? <a id="goto-signup">Sign up</a>
        </div>
      </div>
    </div>
  `;

  bindNavbar(rootEl, navigate);

  // Go to signup link
  rootEl.querySelector('#goto-signup').addEventListener('click', (e) => {
    e.preventDefault();
    navigate('/signup');
  });

  // Form submit
  const form = rootEl.querySelector('#login-form');
  const emailInput = rootEl.querySelector('#login-email');
  const submitBtn = rootEl.querySelector('#login-submit-btn');
  const submitText = rootEl.querySelector('#login-submit-text');
  const spinner = rootEl.querySelector('#login-spinner');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    if (!email) {
      showToast('error', 'Please enter your email.');
      return;
    }

    submitBtn.disabled = true;
    submitText.style.display = 'none';
    spinner.style.display = 'block';

    try {
      await login(email);
      showToast('success', 'Signed in successfully!');
      onAuthSuccess(email);
    } catch (err) {
      const msg = err.message || '';
      // If user not found, redirect to signup
      if (msg.toLowerCase().includes('not found') || msg.toLowerCase().includes('signup')) {
        showToast('info', 'Account not found. Redirecting to sign up…');
        setTimeout(() => navigate('/signup', email), 1200);
      } else {
        showToast('error', msg || 'Login failed.');
      }
    } finally {
      submitBtn.disabled = false;
      submitText.style.display = 'inline';
      spinner.style.display = 'none';
    }
  });
}

/* ============================================
   SIGNUP PAGE
   ============================================ */

export function initSignup(rootEl, navigate, onAuthSuccess, prefillEmail) {
  rootEl.innerHTML = `
    ${renderNavbar('signup')}
    <div class="auth-page" id="auth-page">
      <div class="auth-bg-orb"></div>
      <div class="auth-bg-orb"></div>
      <div class="auth-bg-orb"></div>

      <div class="auth-card glass-panel">
        <div class="auth-logo">
          <div class="auth-logo-icon">⚖️</div>
          <div class="auth-logo-text">Legal<span>AI</span></div>
        </div>

        <h1 class="modal-title">Create account</h1>
        <p class="modal-subtitle">Start your legal research journey today</p>

        <form class="auth-form-container" id="signup-form" autocomplete="off">
          <div class="input-group">
            <label for="signup-name">Full Name</label>
            <input class="input" type="text" id="signup-name" placeholder="John Doe" maxlength="50" required />
          </div>

          <div class="input-group">
            <label for="signup-email">Email Address</label>
            <input class="input" type="email" id="signup-email" placeholder="you@example.com" maxlength="100" required value="${prefillEmail || ''}" />
          </div>

          <button type="submit" class="btn btn-primary btn-lg" id="signup-submit-btn">
            <span id="signup-submit-text">Create Account</span>
            <div class="spinner" id="signup-spinner" style="display: none;"></div>
          </button>
        </form>

        <div class="auth-footer">
          Already have an account? <a id="goto-login">Sign in</a>
        </div>
      </div>
    </div>
  `;

  bindNavbar(rootEl, navigate);

  // Go to login link
  rootEl.querySelector('#goto-login').addEventListener('click', (e) => {
    e.preventDefault();
    navigate('/login');
  });

  // Form submit
  const form = rootEl.querySelector('#signup-form');
  const nameInput = rootEl.querySelector('#signup-name');
  const emailInput = rootEl.querySelector('#signup-email');
  const submitBtn = rootEl.querySelector('#signup-submit-btn');
  const submitText = rootEl.querySelector('#signup-submit-text');
  const spinner = rootEl.querySelector('#signup-spinner');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = nameInput.value.trim();
    const email = emailInput.value.trim();

    if (!name) { showToast('error', 'Please enter your name.'); return; }
    if (!email) { showToast('error', 'Please enter your email.'); return; }

    submitBtn.disabled = true;
    submitText.style.display = 'none';
    spinner.style.display = 'block';

    try {
      await signup(name, email);
      showToast('success', 'Account created! Signing you in…');
      await login(email);
      showToast('success', 'Signed in successfully!');
      onAuthSuccess(email);
    } catch (err) {
      showToast('error', err.message || 'Signup failed.');
    } finally {
      submitBtn.disabled = false;
      submitText.style.display = 'inline';
      spinner.style.display = 'none';
    }
  });
}
