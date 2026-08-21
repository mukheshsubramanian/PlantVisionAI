/**
 * PlantVision AI - Frontend JavaScript Application Logic
 * Integrates:
 * 1. Dedicated Home Page & Visual Showcase
 * 2. Complete Sign In / Sign Up & Session Authentication System
 * 3. Deep Learning Leaf Diagnostic Scanner (Camera & File Dropzone)
 * 4. 115+ Disease Encyclopedia & Treatment Library
 * 5. Agentic AI Plant Health Assistant
 * 6. User-Linked Diagnostic History Logs & Export
 */

document.addEventListener("DOMContentLoaded", () => {
  // --- App State ---
  const state = {
    currentView: "home-view",
    currentFile: null,
    currentScanResult: null,
    activeScanContext: null,
    chatMessages: [],
    diseasesCatalog: {},
    history: [],
    authToken: localStorage.getItem("plantvision_auth_token") || null,
    currentUser: null,
    voiceAutoPlay: localStorage.getItem("plantvision_voice_auto") !== "false",
    isSpeaking: false,
    isListening: false,
    speechSynthesisVoices: []
  };

  // --- Navigation & Core Elements ---
  const navItems = document.querySelectorAll(".nav-item");
  const viewSections = document.querySelectorAll(".view-section");
  const navBrandBtn = document.getElementById("nav-brand-btn");
  const themeToggleBtn = document.getElementById("theme-toggle-btn");
  const systemStatusChip = document.getElementById("system-status-chip");
  const statusLabelText = document.getElementById("status-label-text");
  const toastContainer = document.getElementById("toast-container");

  // --- Front Brand Showcase Elements ---
  const frontEnterScanBtn = document.getElementById("front-enter-scan-btn");
  const frontEnterLibBtn = document.getElementById("front-enter-lib-btn");
  const portalActionBtns = document.querySelectorAll(".portal-action-btn");
  const frontPortalCards = document.querySelectorAll(".front-portal-card");

  // --- Home Page CTA Buttons ---
  const homeStartScanBtn = document.getElementById("home-start-scan-btn");
  const homeBrowseLibBtn = document.getElementById("home-browse-lib-btn");
  const homeTrySamplesBtn = document.getElementById("home-try-samples-btn");
  const ctaBottomScanBtn = document.getElementById("cta-bottom-scan-btn");
  const ctaBottomSignupBtn = document.getElementById("cta-bottom-signup-btn");

  // --- Authentication Header Elements ---
  const authGuestBox = document.getElementById("auth-guest-box");
  const authUserBox = document.getElementById("auth-user-box");
  const openLoginBtn = document.getElementById("open-login-btn");
  const openSignupBtn = document.getElementById("open-signup-btn");
  const userProfileToggleBtn = document.getElementById("user-profile-toggle-btn");
  const userAvatarInitials = document.getElementById("user-avatar-initials");
  const userNameLabel = document.getElementById("user-name-label");
  const userDropdownPopover = document.getElementById("user-dropdown-popover");
  const dropdownAvatarLarge = document.getElementById("dropdown-avatar-large");
  const dropdownUserFullname = document.getElementById("dropdown-user-fullname");
  const dropdownUserEmail = document.getElementById("dropdown-user-email");
  const dropdownMyScansBtn = document.getElementById("dropdown-my-scans-btn");
  const dropdownViewProfileBtn = document.getElementById("dropdown-view-profile-btn");
  const logoutBtn = document.getElementById("logout-btn");

  // --- Authentication Modal Elements ---
  const authModal = document.getElementById("auth-modal");
  const authModalCloseBtn = document.getElementById("auth-modal-close-btn");
  const authModalHeading = document.getElementById("auth-modal-heading");
  const authModalSubheading = document.getElementById("auth-modal-subheading");
  const tabLoginBtn = document.getElementById("tab-login-btn");
  const tabSignupBtn = document.getElementById("tab-signup-btn");
  const authAlert = document.getElementById("auth-alert");
  const authAlertText = document.getElementById("auth-alert-text");
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const loginIdentifierInput = document.getElementById("login-identifier");
  const loginPasswordInput = document.getElementById("login-password");
  const signupFullnameInput = document.getElementById("signup-fullname");
  const signupUsernameInput = document.getElementById("signup-username");
  const signupEmailInput = document.getElementById("signup-email");
  const signupPhoneInput = document.getElementById("signup-phone");
  const signupPasswordInput = document.getElementById("signup-password");
  const loginSubmitBtn = document.getElementById("login-submit-btn");
  const signupSubmitBtn = document.getElementById("signup-submit-btn");
  const fillDemoLoginBtn = document.getElementById("fill-demo-login-btn");
  const forgotPasswordLink = document.getElementById("forgot-password-link");
  const resetPasswordForm = document.getElementById("reset-password-form");
  const forgotStep1 = document.getElementById("forgot-step-1");
  const forgotStep2 = document.getElementById("forgot-step-2");
  const channelEmailBtn = document.getElementById("channel-email-btn");
  const channelSmsBtn = document.getElementById("channel-sms-btn");
  const resetIdentifierLabel = document.getElementById("reset-identifier-label");
  const resetIdentifierHint = document.getElementById("reset-identifier-hint");
  const resetIdentifierIcon = document.getElementById("reset-identifier-icon");
  const resetIdentifierInput = document.getElementById("reset-identifier");
  const sendOtpBtn = document.getElementById("send-otp-btn");
  const otpChannelLabelDisplay = document.getElementById("otp-channel-label-display");
  const otpTargetDisplay = document.getElementById("otp-target-display");
  const otpDeliveryTitle = document.getElementById("otp-delivery-title");
  const otpDeliveryHint = document.getElementById("otp-delivery-hint");
  const changeIdentifierBtn = document.getElementById("change-identifier-btn");
  const resetOtpInput = document.getElementById("reset-otp-input");
  const resendOtpBtn = document.getElementById("resend-otp-btn");
  const resetNewPasswordInput = document.getElementById("reset-new-password");
  const resetConfirmPasswordInput = document.getElementById("reset-confirm-password");
  const resetSubmitBtn = document.getElementById("reset-submit-btn");
  const backToLoginBtn = document.getElementById("back-to-login-btn");
  let selectedOtpChannel = "email";
  let activeResetIdentifier = "";
  let resendCountdown = 60;
  let resendTimerInterval = null;

  // --- Profile Modal Elements ---
  const profileModal = document.getElementById("profile-modal");
  const profileModalCloseBtn = document.getElementById("profile-modal-close-btn");
  const modalProfileCloseBtn = document.getElementById("modal-profile-close-btn");
  const modalProfileLogoutBtn = document.getElementById("modal-profile-logout-btn");
  const modalProfileAvatar = document.getElementById("modal-profile-avatar");
  const modalProfileFullname = document.getElementById("modal-profile-fullname");
  const modalProfileEmail = document.getElementById("modal-profile-email");
  const modalProfileUsername = document.getElementById("modal-profile-username");
  const modalProfileCreated = document.getElementById("modal-profile-created");
  const modalProfileScancount = document.getElementById("modal-profile-scancount");

  // --- Scanner Elements ---
  const dropzoneBox = document.getElementById("dropzone-box");
  const leafFileInput = document.getElementById("leaf-file-input");
  const browseBtn = document.getElementById("browse-btn");
  const dropzoneIdle = document.getElementById("dropzone-idle");
  const dropzonePreview = document.getElementById("dropzone-preview");
  const previewImg = document.getElementById("preview-img");
  const previewFilenameBadge = document.getElementById("preview-filename-badge");
  const reselectBtn = document.getElementById("reselect-btn");
  const analyzeBtn = document.getElementById("analyze-btn");
  const samplesCarouselBar = document.getElementById("samples-carousel-bar");

  // Camera Elements
  const cameraOpenBtn = document.getElementById("camera-open-btn");
  const cameraDrawer = document.getElementById("camera-drawer");
  const cameraCloseBtn = document.getElementById("camera-close-btn");
  const cameraVideo = document.getElementById("camera-video");
  const cameraCanvas = document.getElementById("camera-canvas");
  const cameraCaptureBtn = document.getElementById("camera-capture-btn");
  let cameraStream = null;

  // Results HUD Elements
  const resultsPlaceholder = document.getElementById("results-placeholder");
  const resultsLoader = document.getElementById("results-loader");
  const resultsContent = document.getElementById("results-content");
  const loaderStatusText = document.getElementById("loader-status-text");
  const resCropCategory = document.getElementById("res-crop-category");
  const resDiseaseTitle = document.getElementById("res-disease-title");
  const resSeverityPill = document.getElementById("res-severity-pill");
  const resCategoryBadge = document.getElementById("res-category-badge");
  const resLatencyBadge = document.getElementById("res-latency-badge");
  const resConfidenceVal = document.getElementById("res-confidence-val");
  const gaugeFillCircle = document.getElementById("gauge-fill-circle");
  const uncertaintyAlert = document.getElementById("uncertainty-alert");
  const topkBarsContainer = document.getElementById("topk-bars-container");
  const resSymptomsList = document.getElementById("res-symptoms-list");
  const resCauseText = document.getElementById("res-cause-text");
  const resImmediateTreatment = document.getElementById("res-immediate-treatment");
  const resOrganicTreatment = document.getElementById("res-organic-treatment");
  const resChemicalTreatment = document.getElementById("res-chemical-treatment");
  const resPreventionList = document.getElementById("res-prevention-list");
  const resCautionText = document.getElementById("res-caution-text");
  const askAiAgentBtn = document.getElementById("ask-ai-agent-btn");
  const downloadReportBtn = document.getElementById("download-report-btn");

  // Detail Tabs
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  // Catalog Elements
  const catalogSearchInput = document.getElementById("catalog-search-input");
  const cropFilterChips = document.getElementById("crop-filter-chips");
  const catalogCardsGrid = document.getElementById("catalog-cards-grid");
  const diseaseModal = document.getElementById("disease-modal");
  const modalCropCategory = document.getElementById("modal-crop-category");
  const modalDiseaseTitle = document.getElementById("modal-disease-title");
  const modalBodyContent = document.getElementById("modal-body-content");
  const modalCloseBtn = document.getElementById("modal-close-btn");

  // Assistant Elements
  const noContextState = document.getElementById("no-context-state");
  const activeContextState = document.getElementById("active-context-state");
  const ctxDiseaseBadge = document.getElementById("ctx-disease-badge");
  const ctxCrop = document.getElementById("ctx-crop");
  const ctxSeverity = document.getElementById("ctx-severity");
  const ctxConfidence = document.getElementById("ctx-confidence");
  const clearScanContextBtn = document.getElementById("clear-scan-context-btn");
  const chatMessagesContainer = document.getElementById("chat-messages-container");
  const chatSuggestionsBar = document.getElementById("chat-suggestions-bar");
  const chatInputForm = document.getElementById("chat-input-form");
  const chatInputField = document.getElementById("chat-input-field");
  const clearChatHistoryBtn = document.getElementById("clear-chat-history-btn");
  const presetWorkflowBtns = document.querySelectorAll(".preset-workflow-btn");
  const agentVoiceWaveform = document.getElementById("agent-voice-waveform");
  const voiceModeToggleBtn = document.getElementById("voice-mode-toggle-btn");
  const voiceToggleIcon = document.getElementById("voice-toggle-icon");
  const voiceToggleText = document.getElementById("voice-toggle-text");
  const voiceMicBtn = document.getElementById("voice-mic-btn");

  // History Elements
  const historySubtitleText = document.getElementById("history-subtitle-text");
  const historyListWrapper = document.getElementById("history-list-wrapper");
  const clearAllHistoryBtn = document.getElementById("clear-all-history-btn");

  // --- INITIALIZATION ---
  initTheme();
  checkHealthStatus();
  initAuthSession();
  loadSamplePresets();
  loadDiseasesCatalog();
  loadHistoryLogs();
  initSpeechVoices();
  initVoiceModeUI();
  initSpeechRecognition();

  // --------------------------------------------------------------------------
  // TOAST NOTIFICATION UTILITY
  // --------------------------------------------------------------------------
  function showToast(message, type = "success", duration = 4000) {
    if (!toastContainer) return;
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    
    let icon = "✅";
    if (type === "error") icon = "⚠️";
    if (type === "info") icon = "ℹ️";

    toast.innerHTML = `
      <span class="toast-icon">${icon}</span>
      <span class="toast-text">${message}</span>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.classList.add("toast-fadeout");
      setTimeout(() => toast.remove(), 250);
    }, duration);
  }

  // --------------------------------------------------------------------------
  // NAVIGATION & VIEW ROUTING
  // --------------------------------------------------------------------------
  function switchView(viewId) {
    state.currentView = viewId;
    navItems.forEach(item => {
      item.classList.toggle("active", item.getAttribute("data-view") === viewId);
    });
    viewSections.forEach(section => {
      section.classList.toggle("active", section.id === viewId);
    });
    window.scrollTo({ top: 0, behavior: "smooth" });

    // Close any open popovers
    closeUserDropdown();
  }

  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const view = item.getAttribute("data-view");
      if (view) switchView(view);
    });
  });

  navBrandBtn.addEventListener("click", () => switchView("home-view"));

  // Front Brand Showcase CTA Bindings
  if (frontEnterScanBtn) frontEnterScanBtn.addEventListener("click", () => switchView("scanner-view"));
  if (frontEnterLibBtn) frontEnterLibBtn.addEventListener("click", () => switchView("catalog-view"));

  portalActionBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const target = btn.getAttribute("data-target");
      if (target) switchView(target);
    });
  });

  frontPortalCards.forEach(card => {
    card.addEventListener("click", () => {
      const btn = card.querySelector(".portal-action-btn");
      if (btn) {
        const target = btn.getAttribute("data-target");
        if (target) switchView(target);
      }
    });
  });

  // Home CTA Bindings
  if (homeStartScanBtn) homeStartScanBtn.addEventListener("click", () => switchView("scanner-view"));
  if (homeBrowseLibBtn) homeBrowseLibBtn.addEventListener("click", () => switchView("catalog-view"));
  if (homeTrySamplesBtn) {
    homeTrySamplesBtn.addEventListener("click", () => {
      switchView("scanner-view");
      setTimeout(() => {
        samplesCarouselBar.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 100);
    });
  }
  if (ctaBottomScanBtn) ctaBottomScanBtn.addEventListener("click", () => switchView("scanner-view"));
  if (ctaBottomSignupBtn) {
    ctaBottomSignupBtn.addEventListener("click", () => {
      if (state.currentUser) {
        switchView("scanner-view");
      } else {
        openAuthModal("signup");
      }
    });
  }

  // --------------------------------------------------------------------------
  // THEME TOGGLE
  // --------------------------------------------------------------------------
  function initTheme() {
    const savedTheme = localStorage.getItem("plantvision_theme") || "dark";
    document.body.className = `theme-${savedTheme}`;
  }

  themeToggleBtn.addEventListener("click", () => {
    const isDark = document.body.classList.contains("theme-dark");
    const newTheme = isDark ? "light" : "dark";
    document.body.className = `theme-${newTheme}`;
    localStorage.setItem("plantvision_theme", newTheme);
  });

  // --------------------------------------------------------------------------
  // HEALTH CHECK
  // --------------------------------------------------------------------------
  async function checkHealthStatus() {
    try {
      const res = await fetch("/health");
      if (res.ok) {
        const data = await res.json();
        statusLabelText.textContent = `CNN Ready (${data.device.toUpperCase()})`;
      }
    } catch (e) {
      statusLabelText.textContent = "Backend Offline";
      const dot = systemStatusChip.querySelector(".status-indicator-dot");
      if (dot) dot.style.background = "#f43f5e";
    }
  }

  // --------------------------------------------------------------------------
  // AUTHENTICATION & USER MANAGEMENT
  // --------------------------------------------------------------------------
  async function initAuthSession() {
    const storedUser = localStorage.getItem("plantvision_user");
    if (storedUser) {
      try {
        state.currentUser = JSON.parse(storedUser);
      } catch (e) {
        state.currentUser = null;
      }
    }

    if (state.authToken) {
      try {
        const res = await fetch("/auth/me", {
          headers: { "Authorization": `Bearer ${state.authToken}` }
        });
        if (res.ok) {
          const data = await res.json();
          state.currentUser = data.user;
          localStorage.setItem("plantvision_user", JSON.stringify(data.user));
        } else {
          // Token expired
          handleLogout(false);
        }
      } catch (e) {
        console.warn("Could not verify session:", e);
      }
    }
    updateAuthUI();
  }

  function getInitials(name) {
    if (!name) return "PV";
    const parts = name.trim().split(" ");
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function updateAuthUI() {
    if (state.currentUser) {
      // Show user box, hide guest box
      authGuestBox.classList.add("hidden");
      authUserBox.classList.remove("hidden");

      const initials = getInitials(state.currentUser.full_name);
      userAvatarInitials.textContent = initials;
      userNameLabel.textContent = state.currentUser.full_name || state.currentUser.username;
      
      dropdownAvatarLarge.textContent = initials;
      dropdownUserFullname.textContent = state.currentUser.full_name;
      dropdownUserEmail.textContent = state.currentUser.email;

      // Update Profile Modal fields
      modalProfileAvatar.textContent = initials;
      modalProfileFullname.textContent = state.currentUser.full_name;
      modalProfileEmail.textContent = state.currentUser.email;
      modalProfileUsername.textContent = state.currentUser.username;
      modalProfileCreated.textContent = state.currentUser.created_at ? state.currentUser.created_at.split(" ")[0] : "Active";
      modalProfileScancount.textContent = `${state.history.length} Scans Logged`;

      // Update History view subtitle
      if (historySubtitleText) {
        historySubtitleText.textContent = `Logged in as ${state.currentUser.full_name} (${state.currentUser.email}) — displaying personal field scan logs.`;
      }
    } else {
      // Guest state
      authGuestBox.classList.remove("hidden");
      authUserBox.classList.add("hidden");
      closeUserDropdown();

      if (historySubtitleText) {
        historySubtitleText.textContent = "Review recent leaf scans, diagnoses, confidence scores, and recommendations.";
      }
    }
  }

  function openAuthModal(tab = "login") {
    authModal.classList.remove("hidden");
    hideAuthAlert();
    switchAuthTab(tab);
  }

  function closeAuthModal() {
    authModal.classList.add("hidden");
    hideAuthAlert();
  }

  function switchAuthTab(tab) {
    if (tab === "login") {
      tabLoginBtn.classList.add("active");
      tabSignupBtn.classList.remove("active");
      loginForm.classList.remove("hidden");
      signupForm.classList.add("hidden");
      if (resetPasswordForm) resetPasswordForm.classList.add("hidden");
      authModalHeading.textContent = "Welcome Back to PlantVision";
      authModalSubheading.textContent = "Sign in to access your personal crop scan history and synchronised field records.";
    } else if (tab === "signup") {
      tabLoginBtn.classList.remove("active");
      tabSignupBtn.classList.add("active");
      loginForm.classList.add("hidden");
      signupForm.classList.remove("hidden");
      if (resetPasswordForm) resetPasswordForm.classList.add("hidden");
      authModalHeading.textContent = "Create Free Agronomist Account";
      authModalSubheading.textContent = "Join PlantVision AI to track disease outbreaks, save prescription protocols, and consult our AI expert.";
    } else if (tab === "reset") {
      tabLoginBtn.classList.remove("active");
      tabSignupBtn.classList.remove("active");
      loginForm.classList.add("hidden");
      signupForm.classList.add("hidden");
      if (resetPasswordForm) {
        resetPasswordForm.classList.remove("hidden");
        if (forgotStep1) forgotStep1.classList.remove("hidden");
        if (forgotStep2) forgotStep2.classList.add("hidden");
      }
      authModalHeading.textContent = "Forgot Password Verification";
      authModalSubheading.textContent = "Enter your registered Email ID or Phone Number to receive a 6-digit verification code (OTP).";
    }
  }

  function showAuthAlert(msg, isSuccess = false) {
    authAlertText.textContent = msg;
    authAlert.className = `auth-alert ${isSuccess ? 'success' : ''}`;
    authAlert.classList.remove("hidden");
  }

  function hideAuthAlert() {
    authAlert.classList.add("hidden");
  }

  // Password visibility toggles
  document.querySelectorAll(".toggle-password-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const targetInput = document.getElementById(targetId);
      if (targetInput) {
        if (targetInput.type === "password") {
          targetInput.type = "text";
          btn.textContent = "🙈";
        } else {
          targetInput.type = "password";
          btn.textContent = "👁️";
        }
      }
    });
  });

  openLoginBtn.addEventListener("click", () => openAuthModal("login"));
  openSignupBtn.addEventListener("click", () => openAuthModal("signup"));
  authModalCloseBtn.addEventListener("click", closeAuthModal);
  tabLoginBtn.addEventListener("click", () => switchAuthTab("login"));
  tabSignupBtn.addEventListener("click", () => switchAuthTab("signup"));

  // Close modal when clicking backdrop
  authModal.addEventListener("click", (e) => {
    if (e.target === authModal) closeAuthModal();
  });

  // Login Form Submission
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAuthAlert();
    const identifier = loginIdentifierInput.value.trim();
    const password = loginPasswordInput.value;

    if (!identifier || !password) {
      showAuthAlert("Please enter your username/email and password.");
      return;
    }

    loginSubmitBtn.disabled = true;
    loginSubmitBtn.innerHTML = `<span>Signing in...</span>`;

    try {
      const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username_or_email: identifier,
          password: password
        })
      });

      const data = await res.json();
      loginSubmitBtn.disabled = false;
      loginSubmitBtn.innerHTML = `<span>Sign In to PlantVision</span>`;

      if (!res.ok) {
        showAuthAlert(data.detail || "Invalid login credentials.");
        return;
      }

      // Success
      state.authToken = data.token;
      state.currentUser = data.user;
      localStorage.setItem("plantvision_auth_token", data.token);
      localStorage.setItem("plantvision_user", JSON.stringify(data.user));

      updateAuthUI();
      closeAuthModal();
      showToast(`Welcome back, ${data.user.full_name}! 👋`, "success");
      loadHistoryLogs();

    } catch (err) {
      loginSubmitBtn.disabled = false;
      loginSubmitBtn.innerHTML = `<span>Sign In to PlantVision</span>`;
      showAuthAlert("Network connection error: " + err.message);
    }
  });

  // Sign Up Form Submission
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAuthAlert();
    const fullName = signupFullnameInput.value.trim();
    const username = signupUsernameInput.value.trim();
    const email = signupEmailInput.value.trim();
    const password = signupPasswordInput.value;

    if (!fullName || !username || !email || !password) {
      showAuthAlert("Please complete all registration fields.");
      return;
    }

    if (password.length < 6) {
      showAuthAlert("Password must be at least 6 characters long.");
      return;
    }

    signupSubmitBtn.disabled = true;
    signupSubmitBtn.innerHTML = `<span>Creating Account...</span>`;

    try {
      const res = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,
          username: username,
          email: email,
          phone: signupPhoneInput ? signupPhoneInput.value.trim() || null : null,
          password: password
        })
      });

      const data = await res.json();
      signupSubmitBtn.disabled = false;
      signupSubmitBtn.innerHTML = `<span>Create Free Account</span>`;

      if (!res.ok) {
        showAuthAlert(data.detail || "Registration failed.");
        return;
      }

      // Success
      state.authToken = data.token;
      state.currentUser = data.user;
      localStorage.setItem("plantvision_auth_token", data.token);
      localStorage.setItem("plantvision_user", JSON.stringify(data.user));

      updateAuthUI();
      closeAuthModal();
      showToast(`Welcome to PlantVision AI, ${data.user.full_name}! 🌱`, "success");
      loadHistoryLogs();

    } catch (err) {
      signupSubmitBtn.disabled = false;
      signupSubmitBtn.innerHTML = `<span>Create Free Account</span>`;
      showAuthAlert("Network connection error: " + err.message);
    }
  });

  // Demo Credentials Fill Button
  fillDemoLoginBtn.addEventListener("click", () => {
    loginIdentifierInput.value = "agronomist@plantvision.ai";
    loginPasswordInput.value = "SecurePassword2026!";
    loginForm.dispatchEvent(new Event("submit"));
  });

  // --- Forgot Password & OTP Verification Flow Handlers ---

  function setOtpChannel(channel) {
    selectedOtpChannel = channel;
    if (channel === "email") {
      if (channelEmailBtn) channelEmailBtn.classList.add("active");
      if (channelSmsBtn) channelSmsBtn.classList.remove("active");
      if (resetIdentifierLabel) resetIdentifierLabel.textContent = "Registered Email Address (or Username)";
      if (resetIdentifierInput) resetIdentifierInput.placeholder = "e.g. agronomist@plantvision.ai or username";
      if (resetIdentifierHint) resetIdentifierHint.textContent = "We will dispatch a secure 6-digit one-time passcode (OTP) to your email address.";
      if (resetIdentifierIcon) {
        resetIdentifierIcon.innerHTML = `<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>`;
      }
    } else {
      if (channelSmsBtn) channelSmsBtn.classList.add("active");
      if (channelEmailBtn) channelEmailBtn.classList.remove("active");
      if (resetIdentifierLabel) resetIdentifierLabel.textContent = "Registered Mobile Number (or Username)";
      if (resetIdentifierInput) resetIdentifierInput.placeholder = "e.g. +1 555-0199 or 9876543210";
      if (resetIdentifierHint) resetIdentifierHint.textContent = "We will dispatch a secure 6-digit one-time passcode (OTP) via SMS to your mobile phone.";
      if (resetIdentifierIcon) {
        resetIdentifierIcon.innerHTML = `<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>`;
      }
    }
  }

  if (channelEmailBtn) {
    channelEmailBtn.addEventListener("click", () => setOtpChannel("email"));
  }

  if (channelSmsBtn) {
    channelSmsBtn.addEventListener("click", () => setOtpChannel("sms"));
  }

  function startResendCountdown() {
    if (resendTimerInterval) clearInterval(resendTimerInterval);
    resendCountdown = 60;
    if (resendOtpBtn) {
      resendOtpBtn.classList.add("disabled");
      resendOtpBtn.textContent = `Resend OTP (${resendCountdown}s)`;
    }
    resendTimerInterval = setInterval(() => {
      resendCountdown--;
      if (resendCountdown <= 0) {
        clearInterval(resendTimerInterval);
        resendTimerInterval = null;
        if (resendOtpBtn) {
          resendOtpBtn.classList.remove("disabled");
          resendOtpBtn.textContent = "Resend OTP";
        }
      } else if (resendOtpBtn) {
        resendOtpBtn.textContent = `Resend OTP (${resendCountdown}s)`;
      }
    }, 1000);
  }

  async function requestVerificationOtp(isResend = false) {
    hideAuthAlert();
    const identifier = (isResend ? activeResetIdentifier : (resetIdentifierInput ? resetIdentifierInput.value : "")).trim();

    if (!identifier) {
      showAuthAlert("Please enter your registered Email Address, Mobile Number, or Username.");
      if (resetIdentifierInput) {
        resetIdentifierInput.focus();
        resetIdentifierInput.style.borderColor = "#ef4444";
        setTimeout(() => {
          if (resetIdentifierInput) resetIdentifierInput.style.borderColor = "";
        }, 2000);
      }
      return;
    }

    if (isResend) {
      if (resendOtpBtn) {
        resendOtpBtn.classList.add("disabled");
        resendOtpBtn.textContent = "Sending...";
      }
    } else {
      if (sendOtpBtn) {
        sendOtpBtn.disabled = true;
        sendOtpBtn.innerHTML = `<span class="loading-spinner" style="display:inline-block; width:14px; height:14px; border:2px solid #fff; border-top-color:transparent; border-radius:50%; animation:spin 0.6s linear infinite; margin-right:6px;"></span><span>Dispatching OTP...</span>`;
      }
    }

    try {
      const res = await fetch("/auth/send-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          identifier: identifier,
          channel: selectedOtpChannel || "email"
        })
      });

      const data = await res.json();

      if (isResend) {
        if (resendOtpBtn) resendOtpBtn.textContent = "Resend OTP";
      } else {
        if (sendOtpBtn) {
          sendOtpBtn.disabled = false;
          sendOtpBtn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg><span>Send Verification OTP</span>`;
        }
      }

      if (!res.ok) {
        showAuthAlert(data.detail || "Failed to dispatch OTP passcode.");
        return;
      }

      // Success: Save active session details & transition to Step 2
      activeResetIdentifier = identifier;

      if (otpTargetDisplay) otpTargetDisplay.textContent = data.target || identifier;

      if (otpChannelLabelDisplay) {
        otpChannelLabelDisplay.textContent = data.target_type === "sms" ? "SMS dispatched to:" : "Email dispatched to:";
      }

      if (otpDeliveryTitle) {
        otpDeliveryTitle.textContent = data.target_type === "sms" ? "Check Your Registered Mobile" : "Check Your Registered Inbox";
      }

      if (otpDeliveryHint) {
        if (data.is_real_delivery) {
          otpDeliveryHint.innerHTML = `✅ <strong>Inbox Dispatched:</strong> A secure 6-digit verification code was sent directly to <strong>${data.target}</strong>. Please check your inbox (including Spam/Junk folder) and enter the code below.`;
        } else if (data.target_type === "sms") {
          otpDeliveryHint.innerHTML = `📱 <strong>SMS Gateway Notice:</strong> Real SMS requires Twilio configured in <code>backend/.env</code>. Passcode has been generated for <strong>${data.target}</strong>.`;
        } else {
          otpDeliveryHint.innerHTML = `⚠️ <strong>SMTP Setup Required:</strong> To receive actual emails in your Gmail inbox, configure your Gmail address & App Password in <code>backend/.env</code>.`;
        }
      }

      // Immediately switch views
      if (forgotStep1) forgotStep1.classList.add("hidden");
      if (forgotStep2) forgotStep2.classList.remove("hidden");

      // Clear input and focus it so user enters the code received in email/SMS
      if (resetOtpInput) {
        resetOtpInput.value = "";
        setTimeout(() => resetOtpInput.focus(), 150);
      }

      startResendCountdown();
      showToast(data.message || `Verification OTP sent to ${data.target || identifier}!`, data.is_real_delivery ? "success" : "info");
      if (data.is_real_delivery) {
        showAuthAlert(`✅ Verification code sent directly to your inbox (${data.target}). Enter the 6-digit code below.`, true);
      } else {
        showAuthAlert(`Verification code dispatched for ${data.target}. Enter your 6-digit OTP below to proceed.`, true);
      }

    } catch (err) {
      if (isResend) {
        if (resendOtpBtn) {
          resendOtpBtn.classList.remove("disabled");
          resendOtpBtn.textContent = "Resend OTP";
        }
      } else {
        if (sendOtpBtn) {
          sendOtpBtn.disabled = false;
          sendOtpBtn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg><span>Send Verification OTP</span>`;
        }
      }
      showAuthAlert("Network connection error: " + err.message);
    }
  }

  // Expose to window for inline HTML onclick/onkeydown fallbacks
  window.requestVerificationOtp = requestVerificationOtp;
  window.setOtpChannel = setOtpChannel;

  if (sendOtpBtn) {
    sendOtpBtn.addEventListener("click", (e) => {
      e.preventDefault();
      requestVerificationOtp(false);
    });
  }

  if (resetIdentifierInput) {
    resetIdentifierInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        requestVerificationOtp(false);
      }
    });
  }

  if (resendOtpBtn) {
    resendOtpBtn.addEventListener("click", () => {
      if (resendCountdown > 0 && resendTimerInterval) return;
      requestVerificationOtp(true);
    });
  }

  if (changeIdentifierBtn) {
    changeIdentifierBtn.addEventListener("click", () => {
      hideAuthAlert();
      if (forgotStep2) forgotStep2.classList.add("hidden");
      if (forgotStep1) forgotStep1.classList.remove("hidden");
      if (resetIdentifierInput) {
        resetIdentifierInput.focus();
        resetIdentifierInput.select();
      }
    });
  }



  // Format OTP input to only allow 6 numbers and auto-advance
  if (resetOtpInput) {
    resetOtpInput.addEventListener("input", (e) => {
      e.target.value = e.target.value.replace(/\D/g, "").slice(0, 6);
      if (e.target.value.length === 6 && resetNewPasswordInput) {
        resetNewPasswordInput.focus();
      }
    });
  }

  function openForgotPassword() {
    hideAuthAlert();
    if (loginIdentifierInput && loginIdentifierInput.value.trim() && resetIdentifierInput) {
      resetIdentifierInput.value = loginIdentifierInput.value.trim();
      if (loginIdentifierInput.value.includes("@")) {
        setOtpChannel("email");
      } else if (/^\+?[0-9\s\-()]+$/.test(loginIdentifierInput.value.trim()) && loginIdentifierInput.value.trim().length >= 7) {
        setOtpChannel("sms");
      }
    }
    switchAuthTab("reset");
    if (resetIdentifierInput) {
      setTimeout(() => resetIdentifierInput.focus(), 100);
    }
  }

  window.openForgotPassword = openForgotPassword;
  window.switchAuthTab = switchAuthTab;

  if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener("click", (e) => {
      e.preventDefault();
      openForgotPassword();
    });
  }

  if (backToLoginBtn) {
    backToLoginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideAuthAlert();
      if (resendTimerInterval) {
        clearInterval(resendTimerInterval);
        resendTimerInterval = null;
      }
      switchAuthTab("login");
    });
  }

  // Reset Password Form Submission with OTP Validation
  if (resetPasswordForm) {
    resetPasswordForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      hideAuthAlert();

      // If Step 1 is active, pressing Enter or submit dispatches the OTP
      if (forgotStep1 && !forgotStep1.classList.contains("hidden")) {
        requestVerificationOtp(false);
        return;
      }

      const identifier = activeResetIdentifier || (resetIdentifierInput ? resetIdentifierInput.value.trim() : "");
      const otpVal = resetOtpInput ? resetOtpInput.value.trim() : "";
      const newPassword = resetNewPasswordInput ? resetNewPasswordInput.value : "";
      const confirmPassword = resetConfirmPasswordInput ? resetConfirmPasswordInput.value : "";

      if (!identifier) {
        showAuthAlert("Please request an OTP passcode first.");
        if (forgotStep1) forgotStep1.classList.remove("hidden");
        if (forgotStep2) forgotStep2.classList.add("hidden");
        return;
      }

      if (!otpVal || otpVal.length !== 6) {
        showAuthAlert("Please enter the complete 6-digit verification code (OTP).");
        if (resetOtpInput) resetOtpInput.focus();
        return;
      }

      if (!newPassword || !confirmPassword) {
        showAuthAlert("Please enter and confirm your new password.");
        return;
      }

      if (newPassword.length < 6) {
        showAuthAlert("New password must be at least 6 characters long.");
        return;
      }

      if (newPassword !== confirmPassword) {
        showAuthAlert("Passwords do not match. Please verify and re-type.");
        return;
      }

      resetSubmitBtn.disabled = true;
      resetSubmitBtn.innerHTML = `<span>Verifying & Updating...</span>`;

      try {
        const res = await fetch("/auth/reset-password", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username_or_email: identifier,
            new_password: newPassword,
            otp: otpVal
          })
        });

        const data = await res.json();
        resetSubmitBtn.disabled = false;
        resetSubmitBtn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg><span>Verify OTP & Update Password</span>`;

        if (!res.ok) {
          showAuthAlert(data.detail || "Password reset failed. Please verify your OTP code.");
          return;
        }

        // Reset successful
        if (resendTimerInterval) {
          clearInterval(resendTimerInterval);
          resendTimerInterval = null;
        }

        showToast(data.message || "Password updated successfully! Please sign in. 🔑", "success");
        if (loginIdentifierInput) loginIdentifierInput.value = identifier;
        if (loginPasswordInput) loginPasswordInput.value = "";
        if (resetNewPasswordInput) resetNewPasswordInput.value = "";
        if (resetConfirmPasswordInput) resetConfirmPasswordInput.value = "";
        if (resetOtpInput) resetOtpInput.value = "";
        activeResetIdentifier = "";
        activeOtpCode = "";

        switchAuthTab("login");
        showAuthAlert("Password updated successfully! You can now sign in with your new password.", true);
        if (loginPasswordInput) loginPasswordInput.focus();

      } catch (err) {
        resetSubmitBtn.disabled = false;
        resetSubmitBtn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg><span>Verify OTP & Update Password</span>`;
        showAuthAlert("Network connection error: " + err.message);
      }
    });
  }

  // User Dropdown Popover Handlers
  function toggleUserDropdown() {
    const isHidden = userDropdownPopover.classList.contains("hidden");
    if (isHidden) {
      userDropdownPopover.classList.remove("hidden");
      userProfileToggleBtn.setAttribute("aria-expanded", "true");
    } else {
      closeUserDropdown();
    }
  }

  function closeUserDropdown() {
    if (userDropdownPopover) {
      userDropdownPopover.classList.add("hidden");
      userProfileToggleBtn.setAttribute("aria-expanded", "false");
    }
  }

  userProfileToggleBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleUserDropdown();
  });

  document.addEventListener("click", (e) => {
    if (userDropdownPopover && !userDropdownPopover.contains(e.target) && !userProfileToggleBtn.contains(e.target)) {
      closeUserDropdown();
    }
  });

  dropdownMyScansBtn.addEventListener("click", () => {
    closeUserDropdown();
    switchView("history-view");
  });

  dropdownViewProfileBtn.addEventListener("click", () => {
    closeUserDropdown();
    openProfileModal();
  });

  function openProfileModal() {
    updateAuthUI();
    profileModal.classList.remove("hidden");
  }

  function closeProfileModal() {
    profileModal.classList.add("hidden");
  }

  profileModalCloseBtn.addEventListener("click", closeProfileModal);
  modalProfileCloseBtn.addEventListener("click", closeProfileModal);
  profileModal.addEventListener("click", (e) => {
    if (e.target === profileModal) closeProfileModal();
  });

  // Logout Handlers
  async function handleLogout(showToastMsg = true) {
    if (state.authToken) {
      try {
        await fetch("/auth/logout", {
          method: "POST",
          headers: { "Authorization": `Bearer ${state.authToken}` }
        });
      } catch (e) {
        // Continue clearing local state regardless
      }
    }

    state.authToken = null;
    state.currentUser = null;
    localStorage.removeItem("plantvision_auth_token");
    localStorage.removeItem("plantvision_user");

    updateAuthUI();
    closeProfileModal();
    closeUserDropdown();
    if (showToastMsg) showToast("You have been signed out.", "info");
    loadHistoryLogs();
  }

  logoutBtn.addEventListener("click", () => handleLogout(true));
  modalProfileLogoutBtn.addEventListener("click", () => handleLogout(true));

  // --------------------------------------------------------------------------
  // SAMPLE PRESETS
  // --------------------------------------------------------------------------
  async function loadSamplePresets() {
    try {
      const res = await fetch("/samples");
      if (res.ok) {
        const data = await res.json();
        renderSamplePresets(data.samples || []);
      }
    } catch (e) {
      console.warn("Could not fetch samples:", e);
    }
  }

  function renderSamplePresets(samples) {
    if (!samples.length) {
      samplesCarouselBar.innerHTML = `<div class="sample-loading-pill">No preset samples available.</div>`;
      return;
    }

    samplesCarouselBar.innerHTML = "";
    samples.forEach(sample => {
      const card = document.createElement("div");
      card.className = "sample-pill-card";
      card.innerHTML = `
        <img class="sample-pill-thumb" src="${sample.url}" alt="${sample.name}" loading="lazy">
        <div class="sample-pill-info">
          <span class="sample-pill-name">${sample.name}</span>
          <span class="sample-pill-crop">${sample.crop} • ${sample.category}</span>
        </div>
      `;
      card.addEventListener("click", () => loadSampleImage(sample.url, sample.filename));
      samplesCarouselBar.appendChild(card);
    });
  }

  async function loadSampleImage(url, filename) {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      const file = new File([blob], filename, { type: blob.type || "image/jpeg" });
      setSelectedFile(file);
      runDiagnosis(file);
    } catch (err) {
      showToast("Failed to load sample image: " + err.message, "error");
    }
  }

  // --------------------------------------------------------------------------
  // FILE DROPZONE & IMAGE SELECTION
  // --------------------------------------------------------------------------
  browseBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    leafFileInput.click();
  });

  dropzoneBox.addEventListener("click", () => {
    if (!state.currentFile) leafFileInput.click();
  });

  leafFileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      runDiagnosis(file);
    }
  });

  ["dragenter", "dragover"].forEach(event => {
    dropzoneBox.addEventListener(event, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzoneBox.classList.add("drag-over");
    });
  });

  ["dragleave", "drop"].forEach(event => {
    dropzoneBox.addEventListener(event, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzoneBox.classList.remove("drag-over");
    });
  });

  dropzoneBox.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      setSelectedFile(file);
      runDiagnosis(file);
    }
  });

  reselectBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    leafFileInput.value = "";
    leafFileInput.click();
  });

  analyzeBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    if (state.currentFile) {
      runDiagnosis(state.currentFile);
    } else {
      leafFileInput.click();
    }
  });

  function setSelectedFile(file) {
    if (!file.type.startsWith("image/")) {
      showToast("Please select a valid image file (JPEG, PNG, WEBP).", "error");
      return;
    }
    state.currentFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      previewFilenameBadge.textContent = file.name;
      dropzoneIdle.classList.add("hidden");
      dropzonePreview.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  }

  // --------------------------------------------------------------------------
  // LIVE CAMERA SCANNER
  // --------------------------------------------------------------------------
  cameraOpenBtn.addEventListener("click", async (e) => {
    e.stopPropagation();
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 640 }, height: { ideal: 640 } }
      });
      cameraVideo.srcObject = cameraStream;
      cameraDrawer.classList.remove("hidden");
    } catch (err) {
      showToast("Camera access error: " + err.message, "error");
    }
  });

  function stopCamera() {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      cameraStream = null;
    }
    cameraDrawer.classList.add("hidden");
  }

  cameraCloseBtn.addEventListener("click", stopCamera);

  cameraCaptureBtn.addEventListener("click", () => {
    if (!cameraVideo.videoWidth) return;
    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;
    const ctx = cameraCanvas.getContext("2d");
    ctx.drawImage(cameraVideo, 0, 0);

    cameraCanvas.toBlob((blob) => {
      stopCamera();
      const file = new File([blob], "camera_leaf_scan.jpg", { type: "image/jpeg" });
      setSelectedFile(file);
      runDiagnosis(file);
    }, "image/jpeg", 0.92);
  });

  // --------------------------------------------------------------------------
  // DETAIL TABS SWITCHING
  // --------------------------------------------------------------------------
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabTarget = btn.getAttribute("data-tab");
      tabBtns.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetPane = document.getElementById(tabTarget);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // --------------------------------------------------------------------------
  // CNN INFERENCE DIAGNOSIS
  // --------------------------------------------------------------------------
  async function runDiagnosis(file) {
    resultsPlaceholder.classList.add("hidden");
    resultsContent.classList.add("hidden");
    resultsLoader.classList.remove("hidden");

    const steps = [
      { id: "step-1", text: "1. Preprocessing & Tensor Normalization" },
      { id: "step-2", text: "2. CNN Feature Extraction & Convolution" },
      { id: "step-3", text: "3. Disease Knowledge Mapping" },
      { id: "step-4", text: "4. Formulating Treatment Protocol" }
    ];

    let currentStep = 0;
    const stepInterval = setInterval(() => {
      currentStep++;
      if (currentStep < steps.length) {
        document.querySelectorAll(".loader-step").forEach(s => s.classList.remove("active"));
        const stepEl = document.getElementById(steps[currentStep].id);
        if (stepEl) stepEl.classList.add("active");
        loaderStatusText.textContent = steps[currentStep].text;
      }
    }, 180);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const headers = {};
      if (state.authToken) {
        headers["Authorization"] = `Bearer ${state.authToken}`;
      }

      const response = await fetch("/predict", {
        method: "POST",
        headers: headers,
        body: formData
      });

      clearInterval(stepInterval);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Prediction failed.");
      }

      const result = await response.json();
      state.currentScanResult = result;
      
      setScanContext(result);
      renderDiagnosticResults(result);
      loadHistoryLogs();
      showToast(`Diagnosis Complete: ${result.disease} (${result.confidence_percentage})`, "success");

    } catch (err) {
      clearInterval(stepInterval);
      resultsLoader.classList.add("hidden");
      resultsPlaceholder.classList.remove("hidden");
      showToast("Diagnostic Error: " + err.message, "error");
    }
  }

  // --------------------------------------------------------------------------
  // STRING & BOTANICAL FORMATTING UTILITIES (No Mixed Words)
  // --------------------------------------------------------------------------
  function formatDisplayName(str) {
    if (!str) return "";
    let clean = String(str)
      .replace(/___/g, " • ")
      .replace(/__/g, " ")
      .replace(/_/g, " ")
      .replace(/\(maize\)/gi, "(Maize)")
      .replace(/([a-z])([A-Z])/g, "$1 $2")
      .replace(/\s+/g, " ")
      .trim();

    return clean
      .split(" ")
      .map(word => {
        if (!word) return "";
        if (word.startsWith("(") && word.length > 1) {
          return "(" + word.charAt(1).toUpperCase() + word.slice(2);
        }
        return word.charAt(0).toUpperCase() + word.slice(1);
      })
      .join(" ");
  }

  function getCropEmoji(crop) {
    const c = (crop || "").toLowerCase();
    if (c.includes("tomato")) return "🍅";
    if (c.includes("potato")) return "🥔";
    if (c.includes("corn") || c.includes("maize")) return "🌽";
    if (c.includes("apple")) return "🍎";
    if (c.includes("grape")) return "🍇";
    if (c.includes("pepper")) return "🫑";
    if (c.includes("cherry")) return "🍒";
    if (c.includes("peach")) return "🍑";
    if (c.includes("strawberry")) return "🍓";
    if (c.includes("blueberry")) return "🫐";
    if (c.includes("raspberry")) return "🍇";
    if (c.includes("soybean") || c.includes("bean")) return "🌱";
    if (c.includes("squash") || c.includes("pumpkin")) return "🎃";
    if (c.includes("cucumber")) return "🥒";
    if (c.includes("orange") || c.includes("citrus")) return "🍊";
    if (c.includes("rice")) return "🌾";
    if (c.includes("wheat") || c.includes("barley")) return "🌾";
    if (c.includes("cotton")) return "☁️";
    if (c.includes("coffee")) return "☕";
    if (c.includes("tea")) return "🍵";
    if (c.includes("banana")) return "🍌";
    if (c.includes("cassava")) return "🍠";
    return "🌿";
  }

  function renderDiagnosticResults(res) {
    resultsLoader.classList.add("hidden");
    resultsPlaceholder.classList.add("hidden");
    resultsContent.classList.remove("hidden");

    const cleanCrop = formatDisplayName(res.crop || "Plant");
    const cleanDisease = formatDisplayName(res.disease || "Diagnosed Condition");
    const cleanTitle = cleanDisease;
    const cleanCategory = formatDisplayName(res.category || "Pathogen");
    const cleanSeverity = formatDisplayName(res.severity || "Moderate");

    resCropCategory.textContent = `${cleanCrop} • ${cleanCategory}`;
    resDiseaseTitle.textContent = cleanDisease;
    resSeverityPill.textContent = `${cleanSeverity} Severity`;
    
    resSeverityPill.className = "severity-badge-pill";
    const sevLower = (res.severity || "").toLowerCase();
    if (sevLower.includes("critical") || sevLower.includes("high")) {
      resSeverityPill.classList.add("severity-critical");
    } else if (sevLower.includes("healthy") || sevLower.includes("none") || (res.category || "").toLowerCase() === "healthy") {
      resSeverityPill.classList.add("severity-healthy");
    }

    resCategoryBadge.textContent = `${cleanCategory} Pathogen`;
    resLatencyBadge.textContent = `⚡ ${res.latency_ms || 35}ms`;

    // Confidence Gauge
    const confVal = typeof res.confidence === "number" ? res.confidence : 0.92;
    const confPercent = Math.round(confVal * 1000) / 10;
    resConfidenceVal.textContent = `${confPercent}%`;
    const circumference = 264;
    const offset = circumference - (confVal * circumference);
    gaugeFillCircle.style.strokeDashoffset = offset;

    if (confVal > 0.75) {
      gaugeFillCircle.style.stroke = "var(--accent-emerald)";
    } else if (confVal > 0.45) {
      gaugeFillCircle.style.stroke = "var(--accent-amber)";
    } else {
      gaugeFillCircle.style.stroke = "var(--accent-rose)";
    }

    if (res.is_uncertain) {
      uncertaintyAlert.classList.remove("hidden");
    } else {
      uncertaintyAlert.classList.add("hidden");
    }

    // Side-by-Side Visual Specimen Verification
    const compUserImg = document.getElementById("comp-user-img");
    const compRefImg = document.getElementById("comp-ref-img");
    const compRefLabel = document.getElementById("comp-ref-label");
    const compRefWrapper = document.getElementById("comp-ref-img-wrapper");

    const refImgUrl = res.image_url || (res.disease_id ? `/static/leaf_images/${res.disease_id}.jpg` : '/samples-static/tomato_early_blight.jpg');
    const userScanSrc = (previewImg && previewImg.src && !previewImg.src.includes("data:image/svg")) ? previewImg.src : '/samples-static/tomato_early_blight.jpg';

    if (compUserImg) compUserImg.src = userScanSrc;
    if (compRefImg) compRefImg.src = refImgUrl;
    if (compRefLabel) compRefLabel.textContent = `${cleanDisease} Reference Specimen`;

    if (compRefWrapper) {
      compRefWrapper.onclick = () => {
        openImageLightbox(refImgUrl, cleanDisease, cleanCrop, cleanCategory, true);
      };
    }

    // Foliar Damage & Health Metrics
    const dm = res.damage_metrics || {};
    const healthyPct = typeof dm.healthy_percentage === "number" ? dm.healthy_percentage : 88.5;
    const lesionPct = typeof dm.lesion_percentage === "number" ? dm.lesion_percentage : 11.5;
    const chloroIdx = typeof dm.chlorophyll_index === "number" ? dm.chlorophyll_index : 85.0;
    const damageStage = dm.damage_stage || (lesionPct < 10 ? "Stage 1: Trace Onset (<10%)" : "Stage 2: Mild-Moderate Spread");

    const resDamageStage = document.getElementById("res-damage-stage");
    const resHealthyBar = document.getElementById("res-healthy-bar");
    const resHealthyVal = document.getElementById("res-healthy-val");
    const resLesionBar = document.getElementById("res-lesion-bar");
    const resLesionVal = document.getElementById("res-lesion-val");
    const resChloroBar = document.getElementById("res-chloro-bar");
    const resChloroVal = document.getElementById("res-chloro-val");

    if (resDamageStage) resDamageStage.textContent = damageStage;
    if (resHealthyBar) resHealthyBar.style.width = `${healthyPct}%`;
    if (resHealthyVal) resHealthyVal.textContent = `${healthyPct}%`;
    if (resLesionBar) resLesionBar.style.width = `${lesionPct}%`;
    if (resLesionVal) resLesionVal.textContent = `${lesionPct}%`;
    if (resChloroBar) resChloroBar.style.width = `${Math.min(100, chloroIdx)}%`;
    if (resChloroVal) resChloroVal.textContent = `${chloroIdx} Index`;

    // Top-K Differential Diagnoses
    topkBarsContainer.innerHTML = "";
    if (res.top_k && res.top_k.length) {
      res.top_k.forEach(item => {
        const row = document.createElement("div");
        row.className = "topk-item";
        const itemCrop = formatDisplayName(item.crop || "");
        const itemDisease = formatDisplayName(item.disease_name || item.disease_id || "");
        row.innerHTML = `
          <div class="topk-label-row">
            <span class="topk-name">${itemDisease} ${itemCrop ? `(${itemCrop})` : ''}</span>
            <span class="topk-val">${item.confidence_percentage}</span>
          </div>
          <div class="topk-bar-track">
            <div class="topk-bar-fill" style="width: ${item.confidence * 100}%"></div>
          </div>
        `;
        topkBarsContainer.appendChild(row);
      });
    }

    // Symptoms
    resSymptomsList.innerHTML = "";
    if (res.symptoms && res.symptoms.length) {
      res.symptoms.forEach(symptom => {
        const li = document.createElement("li");
        li.textContent = symptom;
        resSymptomsList.appendChild(li);
      });
    } else {
      resSymptomsList.innerHTML = "<li>No visible pathogenic lesions reported. Plant foliage appears healthy and vigorous.</li>";
    }

    // Causes
    resCauseText.textContent = res.cause || "Pathogen proliferation dependent on temperature, foliage wetness, and airflow.";

    // Treatments (Support both res.solution and res.treatments)
    const sol = res.solution || res.treatments || {};
    const immediate = sol.immediate_action || sol.immediate || "Inspect surrounding foliage and isolate affected plants.";
    const organic = sol.organic || "Apply certified bio-fungicides or botanical copper formulations.";
    const chemical = sol.chemical || "Consult local extension specialist for approved synthetic rotations.";

    resImmediateTreatment.textContent = immediate;
    resOrganicTreatment.textContent = organic;
    resChemicalTreatment.textContent = chemical;

    // Prevention
    resPreventionList.innerHTML = "";
    if (res.prevention && res.prevention.length) {
      res.prevention.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        resPreventionList.appendChild(li);
      });
    } else {
      resPreventionList.innerHTML = "<li>Maintain optimal drip irrigation and avoid overhead foliar watering.</li>";
    }

    // Caution
    resCautionText.textContent = res.caution || "Follow chemical application guidelines and maintain appropriate pre-harvest intervals.";

    // Automatically synchronize scan context for AI Assistant
    setScanContext(res);
  }

  // Ask AI Button Action
  askAiAgentBtn.addEventListener("click", () => {
    switchView("assistant-view");
    if (state.currentScanResult) {
      const autoQuery = `Can you summarize the best organic and chemical treatment plan for ${state.currentScanResult.disease}?`;
      sendChatMessage(autoQuery);
    }
  });

  // Download Report Button Action
  downloadReportBtn.addEventListener("click", () => {
    if (!state.currentScanResult) return;
    const res = state.currentScanResult;
    const sol = res.solution || res.treatments || {};
    const reportContent = `
=====================================================
PLANTVISION AI - DIAGNOSTIC LEAF SUMMARY REPORT
=====================================================
Scan Timestamp: ${res.timestamp || new Date().toLocaleString()}
Crop: ${formatDisplayName(res.crop)}
Pathology: ${formatDisplayName(res.disease)}
Category: ${res.category} Pathogen
Severity: ${res.severity}
Confidence Rating: ${res.confidence_percentage}
Inference Latency: ${res.latency_ms || 35} ms

--- IDENTIFIED SYMPTOMS ---
${(res.symptoms || []).map(s => `• ${s}`).join("\n")}

--- PATHOGEN CAUSE & ETIOLOGY ---
${res.cause || "N/A"}

--- RECOMMENDED TREATMENT PROTOCOLS ---
1. Immediate Response:
   ${sol.immediate_action || sol.immediate || "N/A"}

2. Organic & Biological Solutions:
   ${sol.organic || "N/A"}

3. Chemical Protection Options:
   ${sol.chemical || "N/A"}

--- LONG-TERM PREVENTION ---
${(res.prevention || []).map(p => `• ${p}`).join("\n")}

--- CAUTIONARY ADVISORY ---
${res.caution || "N/A"}
=====================================================
Generated by PlantVision AI Autonomous Pathology Suite
=====================================================
`;
    const blob = new Blob([reportContent], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `PlantVision_Report_${res.crop}_${res.disease.replace(/\s+/g, "_")}.txt`;
    link.click();
    showToast("Diagnostic report downloaded successfully!", "success");
  });

  // --------------------------------------------------------------------------
  // DISEASE ENCYCLOPEDIA & CATALOG (SEPARATE BOXES)
  // --------------------------------------------------------------------------
  async function loadDiseasesCatalog() {
    try {
      const res = await fetch("/diseases");
      if (res.ok) {
        const data = await res.json();
        state.diseasesCatalog = data.diseases || {};
        renderCatalogCards(state.diseasesCatalog);
      }
    } catch (e) {
      console.warn("Could not load catalog:", e);
    }
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function renderCatalogCards(diseasesMap, filterText = "", filterCrop = "all") {
    if (!catalogCardsGrid) return;
    catalogCardsGrid.innerHTML = "";
    const entries = Object.entries(diseasesMap || {});

    const cleanFilterText = (filterText || "").trim().toLowerCase();
    const searchTokens = cleanFilterText ? cleanFilterText.split(/\s+/).filter(Boolean) : [];
    const filterCropLower = (filterCrop || "all").trim().toLowerCase();

    const filtered = entries.filter(([key, item]) => {
      // 1. Crop category match check
      const cropGroup = (item.crop_group || "").toLowerCase();
      const cropCat = (item.crop_category || "").toLowerCase();
      const cropName = (item.crop || "").toLowerCase();

      const cropMatch = filterCropLower === "all" ||
                        cropGroup === filterCropLower ||
                        cropCat === filterCropLower ||
                        cropName === filterCropLower ||
                        cropName.includes(filterCropLower);

      // 2. Multi-Token Search check
      if (searchTokens.length > 0) {
        const formattedTitle = formatDisplayName(item.disease_name || key);
        const formattedCrop = formatDisplayName(item.crop || "");
        const formattedCategory = formatDisplayName(item.category || "");
        const symptomsText = Array.isArray(item.symptoms) ? item.symptoms.join(" ") : (item.symptoms || "");
        const causeText = item.cause || "";
        const pathogenText = item.pathogen || "";
        const sciName = item.scientific_name || "";
        const sol = item.solution || item.treatments || {};
        const treatmentsText = `${sol.immediate_action || ''} ${sol.organic || ''} ${sol.chemical || ''}`;
        const keyClean = key.replace(/_/g, " ");

        // Build comprehensive searchable corpus
        const searchableCorpus = `${formattedTitle} ${formattedCrop} ${formattedCategory} ${item.crop_group || ''} ${pathogenText} ${sciName} ${symptomsText} ${causeText} ${treatmentsText} ${keyClean} ${item.severity_level || ''}`.toLowerCase();

        // Every token must match somewhere in the disease profile
        const textMatches = searchTokens.every(tok => searchableCorpus.includes(tok));
        
        // If searching with keywords, match if text matches
        return textMatches && (filterCropLower === "all" || cropMatch || searchTokens.length > 0);
      }

      return cropMatch;
    });

    // Update Counter Badge
    const catalogCountNum = document.getElementById("catalog-count-num");
    const catalogSearchClearBtn = document.getElementById("catalog-search-clear-btn");
    
    if (catalogCountNum) {
      catalogCountNum.textContent = filtered.length;
    }

    if (catalogSearchClearBtn) {
      if (cleanFilterText) {
        catalogSearchClearBtn.classList.remove("hidden");
      } else {
        catalogSearchClearBtn.classList.add("hidden");
      }
    }

    if (!filtered.length) {
      catalogCardsGrid.innerHTML = `
        <div class="catalog-empty-msg">
          <div class="empty-icon" style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="margin-bottom: 0.5rem; color: var(--text-primary);">No Disease Records Found</h3>
          <p style="color: var(--text-secondary); margin-bottom: 1.25rem;">No disease profiles matched "<strong>${escapeHtml(cleanFilterText)}</strong>"${filterCropLower !== 'all' ? ` in the <em>${escapeHtml(filterCrop)}</em> category` : ''}.</p>
          <button type="button" class="btn btn-sm btn-primary reset-catalog-filter-btn" id="reset-catalog-filter-btn">
            Clear Search & Show All 115 Diseases
          </button>
        </div>
      `;

      const resetBtn = document.getElementById("reset-catalog-filter-btn");
      if (resetBtn) {
        resetBtn.addEventListener("click", () => {
          if (catalogSearchInput) catalogSearchInput.value = "";
          if (cropFilterChips) {
            cropFilterChips.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
            const allChip = cropFilterChips.querySelector('[data-crop="all"]');
            if (allChip) allChip.classList.add("active");
          }
          renderCatalogCards(state.diseasesCatalog, "", "all");
        });
      }
      return;
    }

    filtered.forEach(([key, item]) => {
      const card = document.createElement("div");
      card.className = "disease-card";

      const cleanCrop = formatDisplayName(item.crop || "Plant");
      const cleanTitle = formatDisplayName(item.disease_name || key);
      const cleanCategory = item.category || "Pathogen";
      const cleanSeverity = item.severity_level || item.severity || "Moderate";
      const cropEmoji = getCropEmoji(item.crop);

      const sol = item.solution || item.treatments || {};
      const firstSymptom = (item.symptoms && item.symptoms.length)
        ? item.symptoms[0]
        : "Visible foliar lesions, spots, or chlorosis.";
      const causeText = item.cause || "Pathogen proliferation driven by environmental moisture and host susceptibility.";
      const treatmentText = sol.immediate_action || sol.immediate || sol.organic || "Prune infected tissue and apply protective bio-fungicide.";

      const sevLower = cleanSeverity.toLowerCase();
      const sevClass = (cleanCategory === "Healthy" || sevLower === "none") ? "severity-healthy" : `severity-${sevLower}`;

      card.innerHTML = `
        <!-- Leaf Specimen Image Box -->
        <div class="disease-card-thumb-box" title="Click to view full uncropped original leaf specimen in high resolution">
          <img src="${item.image_url || `/static/leaf_images/${key}.jpg`}" alt="${cleanTitle}" class="disease-card-img" loading="lazy" onerror="this.onerror=null;this.src='/samples-static/tomato_healthy.jpg';">
          <div class="photo-specimen-ribbon">
            <span class="ribbon-icon">🌿</span>
            <span>Original Leaf Photo</span>
          </div>
          <div class="full-img-zoom-btn">
            <span>🔍 Zoom</span>
          </div>
          <div class="thumb-crop-badge">
            <span class="crop-emoji">${cropEmoji}</span>
            <span>${cleanCrop}</span>
          </div>
          <div class="thumb-category-tag ${cleanCategory === 'Healthy' ? 'tag-healthy' : ''}">${cleanCategory}</div>
        </div>

        <!-- Card Top Header Box -->
        <div class="disease-card-header">
          <div class="crop-badge-box">
            <span class="crop-emoji">${cropEmoji}</span>
            <span class="crop-name-text">${cleanCrop}</span>
          </div>
          <div class="card-badges-group">
            <span class="pathogen-pill ${cleanCategory === 'Healthy' ? 'pill-healthy' : ''}">${cleanCategory}</span>
            <span class="severity-pill ${sevClass}">${cleanSeverity}</span>
          </div>
        </div>

        <!-- Disease Title & Scientific Name -->
        <div class="disease-title-box">
          <h3 class="disease-card-title">${cleanTitle}</h3>
          <div class="scientific-name-line">
            <span>🔬</span>
            <em>${item.scientific_name || item.pathogen || 'Botanical Pathology'}</em>
          </div>
        </div>

        <!-- Distinct Mini Info Boxes -->
        <div class="disease-card-boxes">
          <!-- Box 1: Symptoms Box -->
          <div class="info-mini-box symptoms-mini-box">
            <div class="mini-box-title"><span class="box-icon">🔍</span> Visual Symptoms</div>
            <p class="mini-box-desc">${firstSymptom}</p>
          </div>

          <!-- Box 2: Cause Box -->
          <div class="info-mini-box cause-mini-box">
            <div class="mini-box-title"><span class="box-icon">⚡</span> Pathogen Etiology</div>
            <p class="mini-box-desc">${causeText}</p>
          </div>

          <!-- Box 3: Treatment Solution Box -->
          <div class="info-mini-box treatment-mini-box">
            <div class="mini-box-title"><span class="box-icon">💊</span> Primary Treatment</div>
            <p class="mini-box-desc">${treatmentText}</p>
          </div>
        </div>

        <!-- Card Action Footer Box -->
        <div class="disease-card-footer">
          <button type="button" class="btn btn-primary btn-sm view-details-btn">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            <span>View Details</span>
          </button>
          <button type="button" class="btn btn-secondary btn-sm scan-leaf-btn" title="Run AI CNN detection on this authentic leaf photo">
            <span>⚡ Test in AI Scanner</span>
          </button>
          <button type="button" class="btn btn-outline btn-sm compare-card-btn" title="Compare with your scanned leaf side-by-side">
            <span>⚖️ Compare</span>
          </button>
        </div>
      `;

      const cardImgUrl = item.image_url || `/static/leaf_images/${key}.jpg`;

      // Full Image Lightbox click on card image box
      card.querySelector(".disease-card-thumb-box").addEventListener("click", (e) => {
        e.stopPropagation();
        openImageLightbox(cardImgUrl, cleanTitle, cleanCrop, cleanCategory, false);
      });

      // Test in AI Scanner Button Listener
      card.querySelector(".scan-leaf-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        switchView("scanner-view");
        loadSampleImage(cardImgUrl, `${key}.jpg`);
        showToast(`Loading authentic ${cleanTitle} leaf photo into AI Scanner...`, "info");
      });

      // Compare Button Listener
      card.querySelector(".compare-card-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        openImageLightbox(cardImgUrl, cleanTitle, cleanCrop, cleanCategory, true);
      });

      // Button Event Listeners
      card.querySelector(".view-details-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        item.disease_id = key;
        openDiseaseModal(item);
      });

      catalogCardsGrid.appendChild(card);
    });
  }

  // Catalog Search & Filters
  function triggerCatalogSearch() {
    const activeChip = cropFilterChips ? cropFilterChips.querySelector(".filter-chip.active") : null;
    const cropCategory = activeChip ? activeChip.getAttribute("data-crop") : "all";
    const query = catalogSearchInput ? catalogSearchInput.value : "";
    renderCatalogCards(state.diseasesCatalog, query, cropCategory);
  }

  if (catalogSearchInput) {
    catalogSearchInput.addEventListener("input", triggerCatalogSearch);
    catalogSearchInput.addEventListener("keyup", triggerCatalogSearch);
    catalogSearchInput.addEventListener("change", triggerCatalogSearch);
    catalogSearchInput.addEventListener("search", triggerCatalogSearch);
  }

  const catalogSearchClearBtn = document.getElementById("catalog-search-clear-btn");
  if (catalogSearchClearBtn) {
    catalogSearchClearBtn.addEventListener("click", () => {
      if (catalogSearchInput) {
        catalogSearchInput.value = "";
        catalogSearchInput.focus();
      }
      triggerCatalogSearch();
    });
  }

  if (cropFilterChips) {
    cropFilterChips.querySelectorAll(".filter-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        cropFilterChips.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        triggerCatalogSearch();
      });
    });
  }

  function openDiseaseModal(item) {
    const cleanCrop = formatDisplayName(item.crop || "Plant");
    const cleanTitle = formatDisplayName(item.disease_name || "Pathology Details");
    const cleanCategory = item.category || "Pathology";
    const cleanSeverity = item.severity_level || item.severity || "Moderate";
    const cropEmoji = getCropEmoji(item.crop);

    modalCropCategory.textContent = `${cropEmoji} ${cleanCrop} • ${cleanCategory}`;
    modalDiseaseTitle.textContent = cleanTitle;

    const sol = item.solution || item.treatments || {};
    const immediateAction = sol.immediate_action || sol.immediate || "Isolate affected plants and sanitize pruning shears with 70% isopropyl alcohol.";
    const organicAction = sol.organic || "Apply certified bio-fungicides (e.g. Bacillus subtilis, neem oil, copper octanoate) every 7 days.";
    const chemicalAction = sol.chemical || "Apply registered protective or systemic fungicides rotating FRAC groups to prevent pathogen resistance.";

    const symptomsList = (item.symptoms && item.symptoms.length)
      ? item.symptoms.map(s => `<li class="modal-symptom-item">${s}</li>`).join("")
      : '<li class="modal-symptom-item">No specific visual symptoms noted. Inspect leaf margins and undersides.</li>';

    const preventionList = (item.prevention && item.prevention.length)
      ? item.prevention.map(p => `<li class="modal-prevention-item">${p}</li>`).join("")
      : '<li class="modal-prevention-item">Ensure proper air circulation, avoid overhead foliar watering, and practice crop rotation.</li>';

    const questions = item.recommended_questions || [
      `What is the most effective organic spray recipe for ${cleanTitle}?`,
      `Can I safely consume harvest from a plant infected with ${cleanTitle}?`,
      `How can I prevent ${cleanTitle} from spreading to adjacent crops?`
    ];

    const questionsHtml = questions.map(q => `
      <button type="button" class="modal-question-chip" data-query="${q}">
        <span>💬 ${q}</span>
        <span class="arrow-icon">→</span>
      </button>
    `).join("");

    const sevLower = cleanSeverity.toLowerCase();
    const sevClass = (cleanCategory === "Healthy" || sevLower === "none") ? "severity-healthy" : `severity-${sevLower}`;

    const modalImgUrl = item.image_url || (item.disease_id ? `/static/leaf_images/${item.disease_id}.jpg` : '/samples-static/tomato_healthy.jpg');

    modalBodyContent.innerHTML = `
      <div class="modal-detail-wrapper">
        <!-- Specimen Leaf Image Showcase Box -->
        <div class="modal-info-box modal-image-showcase-box">
          <div class="modal-image-wrapper" title="Click to view full uncropped original leaf photo in high resolution">
            <img src="${modalImgUrl}" alt="${cleanTitle}" class="modal-leaf-img" onerror="this.onerror=null;this.src='/samples-static/tomato_healthy.jpg';">
            <div class="photo-specimen-ribbon modal-ribbon">
              <span class="ribbon-icon">🌿</span>
              <span>Authentic Botanical Leaf Photograph</span>
            </div>
            <div class="modal-zoom-hint-btn">
              <span>🔍 Full Screen View</span>
            </div>
            <div class="modal-image-badge-row">
              <span class="modal-leaf-badge">${cropEmoji} ${cleanCrop} Specimen</span>
              <span class="modal-leaf-severity ${sevClass}">${cleanSeverity} Stage</span>
            </div>
          </div>
          <div class="modal-image-action-bar">
            <button type="button" class="btn btn-secondary btn-sm modal-scan-this-leaf-btn">
              <span>⚡ Test this Leaf Photo in AI Scanner</span>
            </button>
            <button type="button" class="btn btn-outline btn-sm modal-zoom-specimen-btn">
              <span>🔍 Open Lightbox & Compare</span>
            </button>
          </div>
        </div>

        <!-- Top Classification & Header Box -->
        <div class="modal-info-box header-summary-box">
          <div class="header-badge-row">
            <span class="crop-tag-large">${cropEmoji} ${cleanCrop}</span>
            <span class="pathogen-pill pill-large ${cleanCategory === 'Healthy' ? 'pill-healthy' : ''}">${cleanCategory} Pathogen</span>
            <span class="severity-pill pill-large ${sevClass}">
              ${cleanSeverity} Severity
            </span>
          </div>
          <div class="scientific-taxonomy-box">
            <span class="label">Taxonomy & Vector:</span>
            <strong>${item.scientific_name || cleanCrop}</strong> • <em>${item.pathogen || 'Active Pathogen'}</em>
          </div>
          ${item.severity_score ? `
            <div class="severity-meter-row">
              <span class="meter-label">Severity Impact Rating:</span>
              <div class="meter-bar-track">
                <div class="meter-bar-fill ${sevClass}" style="width: ${item.severity_score}%"></div>
              </div>
              <span class="meter-val">${item.severity_score}/100</span>
            </div>
          ` : ''}
        </div>

        <!-- Box 1: Visual Symptoms Box -->
        <div class="modal-info-box symptoms-box">
          <div class="box-header">
            <span class="box-icon">🔍</span>
            <h4>Identified Foliar Symptoms & Visual Markers</h4>
          </div>
          <ul class="modal-symptoms-list">
            ${symptomsList}
          </ul>
        </div>

        <!-- Box 2: Cause & Environmental Biology Box -->
        <div class="modal-info-box cause-box">
          <div class="box-header">
            <span class="box-icon">⚡</span>
            <h4>Pathogen Biology, Inoculum & Weather Triggers</h4>
          </div>
          <p class="box-text">${item.cause || 'Pathogen development driven by surface moisture, warm temperatures, and stagnant airflow.'}</p>
        </div>

        <!-- Box 3: Tri-Tier Treatment Protocol Box -->
        <div class="modal-info-box treatments-box">
          <div class="box-header">
            <span class="box-icon">💊</span>
            <h4>Actionable Prescription & Treatment Plan</h4>
          </div>
          <div class="treatment-sub-boxes">
            <div class="treatment-sub-box immediate-sub-box">
              <div class="sub-box-title">🚨 1. Immediate Sanitation & Physical Response</div>
              <p>${immediateAction}</p>
            </div>
            <div class="treatment-sub-box organic-sub-box">
              <div class="sub-box-title">🌿 2. Organic & Biological Solutions (OMRI Certified)</div>
              <p>${organicAction}</p>
            </div>
            <div class="treatment-sub-box chemical-sub-box">
              <div class="sub-box-title">🧪 3. Synthetic Fungicides & Spray Rotation</div>
              <p>${chemicalAction}</p>
            </div>
          </div>
        </div>

        <!-- Box 4: Prevention Box -->
        <div class="modal-info-box prevention-box">
          <div class="box-header">
            <span class="box-icon">🛡️</span>
            <h4>Cultural Prevention & Sanitation Checklist</h4>
          </div>
          <ul class="modal-prevention-list">
            ${preventionList}
          </ul>
        </div>

        <!-- Box 5: Caution Advisory Box -->
        ${item.caution ? `
          <div class="modal-info-box caution-box">
            <div class="box-header">
              <span class="box-icon">⚠️</span>
              <h4>Safety & Chemical Resistance Advisory</h4>
            </div>
            <div class="modal-caution-text">${item.caution}</div>
          </div>
        ` : ''}

        <!-- Box 6: Interactive Ask AI Prompt Box -->
        <div class="modal-info-box ai-prompt-box">
          <div class="box-header">
            <span class="box-icon">🤖</span>
            <h4>Consult AI Plant Health Agent</h4>
          </div>
          <p class="ai-prompt-sub">Click any question below to immediately ask the AI Plant Assistant:</p>
          <div class="modal-ai-questions">
            ${questionsHtml}
          </div>
        </div>
      </div>
    `;

    // Click on modal image wrapper or zoom button to open full Lightbox
    const modalImageWrapper = modalBodyContent.querySelector(".modal-image-wrapper");
    if (modalImageWrapper) {
      modalImageWrapper.addEventListener("click", () => {
        openImageLightbox(modalImgUrl, cleanTitle, cleanCrop, cleanCategory);
      });
    }

    const modalZoomBtn = modalBodyContent.querySelector(".modal-zoom-specimen-btn");
    if (modalZoomBtn) {
      modalZoomBtn.addEventListener("click", () => {
        openImageLightbox(modalImgUrl, cleanTitle, cleanCrop, cleanCategory);
      });
    }

    // Modal Test in AI Scanner button
    const modalScanBtn = modalBodyContent.querySelector(".modal-scan-this-leaf-btn");
    if (modalScanBtn) {
      modalScanBtn.addEventListener("click", () => {
        diseaseModal.classList.add("hidden");
        switchView("scanner-view");
        loadSampleImage(modalImgUrl, `${item.disease_id || "leaf"}.jpg`);
        showToast(`Loading authentic ${cleanTitle} leaf photo into AI Scanner...`, "info");
      });
    }

    // Attach click listeners to question chips in modal
    modalBodyContent.querySelectorAll(".modal-question-chip").forEach(btn => {
      btn.addEventListener("click", () => {
        const query = btn.getAttribute("data-query");
        diseaseModal.classList.add("hidden");
        switchView("assistant-view");
        setScanContext({
          disease: cleanTitle,
          crop: cleanCrop,
          category: cleanCategory,
          severity: cleanSeverity,
          confidence_percentage: "100%"
        });
        if (query) sendChatMessage(query);
      });
    });

    diseaseModal.classList.remove("hidden");
  }

  modalCloseBtn.addEventListener("click", () => diseaseModal.classList.add("hidden"));
  diseaseModal.addEventListener("click", (e) => {
    if (e.target === diseaseModal) diseaseModal.classList.add("hidden");
  });

  // --------------------------------------------------------------------------
  // FULL LEAF SPECIMEN LIGHTBOX & DUAL COMPARISON MODAL
  // --------------------------------------------------------------------------
  const imageLightboxModal = document.getElementById("image-lightbox-modal");
  const lightboxSingleView = document.getElementById("lightbox-single-view");
  const lightboxDualView = document.getElementById("lightbox-dual-view");
  const toggleSingleRefBtn = document.getElementById("toggle-single-ref-btn");
  const toggleDualCompBtn = document.getElementById("toggle-dual-comp-btn");
  const lightboxFullImg = document.getElementById("lightbox-full-img");
  const lightboxUserScanImg = document.getElementById("lightbox-user-scan-img");
  const lightboxRefDualImg = document.getElementById("lightbox-ref-dual-img");
  const lightboxCropBadge = document.getElementById("lightbox-crop-badge");
  const lightboxDiseaseTitle = document.getElementById("lightbox-disease-title");
  const lightboxCloseBtn = document.getElementById("lightbox-close-btn");
  const lightboxCloseBottomBtn = document.getElementById("lightbox-close-bottom-btn");
  const lightboxAskAiBtn = document.getElementById("lightbox-ask-ai-btn");

  let activeLightboxContext = null;

  function setLightboxMode(mode) {
    if (mode === "dual") {
      if (lightboxSingleView) lightboxSingleView.classList.add("hidden");
      if (lightboxDualView) lightboxDualView.classList.remove("hidden");
      if (toggleDualCompBtn) {
        toggleDualCompBtn.classList.add("btn-primary", "active");
        toggleDualCompBtn.classList.remove("btn-outline");
      }
      if (toggleSingleRefBtn) {
        toggleSingleRefBtn.classList.remove("btn-primary", "active");
        toggleSingleRefBtn.classList.add("btn-outline");
      }
    } else {
      if (lightboxSingleView) lightboxSingleView.classList.remove("hidden");
      if (lightboxDualView) lightboxDualView.classList.add("hidden");
      if (toggleSingleRefBtn) {
        toggleSingleRefBtn.classList.add("btn-primary", "active");
        toggleSingleRefBtn.classList.remove("btn-outline");
      }
      if (toggleDualCompBtn) {
        toggleDualCompBtn.classList.remove("btn-primary", "active");
        toggleDualCompBtn.classList.add("btn-outline");
      }
    }
  }

  if (toggleSingleRefBtn) {
    toggleSingleRefBtn.addEventListener("click", () => setLightboxMode("single"));
  }
  if (toggleDualCompBtn) {
    toggleDualCompBtn.addEventListener("click", () => setLightboxMode("dual"));
  }

  function openImageLightbox(imgUrl, diseaseTitle, cropName, category, startInDualMode = false) {
    if (!imageLightboxModal) return;
    activeLightboxContext = { imgUrl, diseaseTitle, cropName, category };
    
    const cropEmoji = getCropEmoji(cropName);
    if (lightboxFullImg) lightboxFullImg.src = imgUrl;
    if (lightboxRefDualImg) lightboxRefDualImg.src = imgUrl;

    const userScanSrc = (previewImg && previewImg.src && !previewImg.src.includes("data:image/svg"))
      ? previewImg.src
      : '/samples-static/tomato_early_blight.jpg';
    if (lightboxUserScanImg) lightboxUserScanImg.src = userScanSrc;

    if (lightboxCropBadge) lightboxCropBadge.textContent = `${cropEmoji} ${cropName} • ${category}`;
    if (lightboxDiseaseTitle) lightboxDiseaseTitle.textContent = `${diseaseTitle} (Reference Specimen)`;
    
    setLightboxMode(startInDualMode ? "dual" : "single");
    imageLightboxModal.classList.remove("hidden");
  }

  function closeImageLightbox() {
    if (!imageLightboxModal) return;
    imageLightboxModal.classList.add("hidden");
  }

  if (lightboxCloseBtn) lightboxCloseBtn.addEventListener("click", closeImageLightbox);
  if (lightboxCloseBottomBtn) lightboxCloseBottomBtn.addEventListener("click", closeImageLightbox);
  if (imageLightboxModal) {
    imageLightboxModal.addEventListener("click", (e) => {
      if (e.target === imageLightboxModal) closeImageLightbox();
    });
  }

  if (lightboxAskAiBtn) {
    lightboxAskAiBtn.addEventListener("click", () => {
      closeImageLightbox();
      if (activeLightboxContext) {
        switchView("assistant-view");
        setScanContext({
          disease: activeLightboxContext.diseaseTitle,
          crop: activeLightboxContext.cropName,
          category: activeLightboxContext.category,
          severity: "Specimen Inspection",
          confidence_percentage: "100%"
        });
        sendChatMessage(`Can you describe the visual lesion markers and treatment for this ${activeLightboxContext.diseaseTitle} leaf?`);
      }
    });
  }

  // --------------------------------------------------------------------------
  // AI PLANT HEALTH ASSISTANT & VOICE INTERACTION ENGINE
  // --------------------------------------------------------------------------

  // 1. Initialize Speech Synthesis Voices
  function initSpeechVoices() {
    if (!('speechSynthesis' in window)) return;
    
    function loadVoices() {
      state.speechSynthesisVoices = window.speechSynthesis.getVoices() || [];
    }

    loadVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }

  // 2. Setup Voice Mode Auto-Speak Toggle UI
  function initVoiceModeUI() {
    if (!voiceModeToggleBtn) return;
    
    updateVoiceToggleState(state.voiceAutoPlay);

    voiceModeToggleBtn.addEventListener("click", () => {
      state.voiceAutoPlay = !state.voiceAutoPlay;
      localStorage.setItem("plantvision_voice_auto", state.voiceAutoPlay);
      updateVoiceToggleState(state.voiceAutoPlay);
      
      if (!state.voiceAutoPlay) {
        stopSpeech();
        showToast("AI Voice speech output disabled (Muted).", "info");
      } else {
        showToast("AI Voice speech output enabled! The bot will speak aloud.", "success");
      }
    });

    // Wire up initial welcome message Listen button if present
    const initialListenBtn = chatMessagesContainer?.querySelector(".btn-audio-speak");
    if (initialListenBtn) {
      initialListenBtn.addEventListener("click", () => {
        const welcomeText = "Hello! I am your PlantVision AI Health Agent. I can speak and converse with you in plain language about your crops, tailored organic remedies, fungicide rotations, and long-term plant care. How can I assist your garden or crops today? You can type below or click the microphone to talk!";
        speakTextMessage(welcomeText, initialListenBtn);
      });
    }
  }

  function updateVoiceToggleState(isActive) {
    if (!voiceModeToggleBtn) return;
    if (isActive) {
      voiceModeToggleBtn.classList.add("active");
      voiceModeToggleBtn.classList.remove("muted");
      if (voiceToggleIcon) voiceToggleIcon.textContent = "🔊";
      if (voiceToggleText) voiceToggleText.textContent = "Voice: ON";
    } else {
      voiceModeToggleBtn.classList.remove("active");
      voiceModeToggleBtn.classList.add("muted");
      if (voiceToggleIcon) voiceToggleIcon.textContent = "🔇";
      if (voiceToggleText) voiceToggleText.textContent = "Voice: OFF";
    }
  }

  // 3. Clean raw markdown & emojis into smooth, natural human speech
  function cleanTextForSpeech(raw) {
    if (!raw) return "";
    return raw
      .replace(/###\s+/g, ". ")
      .replace(/##\s+/g, ". ")
      .replace(/#\s+/g, ". ")
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/\*(.*?)\*/g, "$1")
      .replace(/_{1,2}(.*?)_{1,2}/g, "$1")
      .replace(/`{1,3}(.*?)`{1,3}/gs, "$1")
      .replace(/<[^>]+>/g, " ")
      .replace(/^\s*[\-\*•]\s+/gm, ", ")
      .replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F1E0}-\u{1F1FF}\u{1FA00}-\u{1FAFF}]/gu, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  // 4. Voice Speech Synthesis Playback
  function speakTextMessage(text, triggerBtn = null) {
    if (!('speechSynthesis' in window)) {
      showToast("Speech synthesis is not supported on this browser.", "warning");
      return;
    }

    // If already speaking the current message, stop it
    if (state.isSpeaking && triggerBtn && triggerBtn.classList.contains("speaking")) {
      stopSpeech();
      return;
    }

    stopSpeech();

    const clean = cleanTextForSpeech(text);
    if (!clean) return;

    state.isSpeaking = true;

    if (agentVoiceWaveform) {
      agentVoiceWaveform.classList.remove("hidden");
    }

    if (triggerBtn) {
      triggerBtn.classList.add("speaking");
      triggerBtn.innerHTML = `<span>⏹️ Stop</span>`;
    }

    const utterance = new SpeechSynthesisUtterance(clean);
    
    // Choose natural sounding English voice if available
    const voices = state.speechSynthesisVoices.length ? state.speechSynthesisVoices : window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => 
      (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Jenny") || v.name.includes("Aria") || v.name.includes("Samantha") || v.name.includes("Zira")) &&
      v.lang.startsWith("en")
    ) || voices.find(v => v.lang.startsWith("en")) || voices[0];

    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    utterance.rate = 1.0;
    utterance.pitch = 1.02;

    const resetUI = () => {
      state.isSpeaking = false;
      if (agentVoiceWaveform) agentVoiceWaveform.classList.add("hidden");
      if (triggerBtn) {
        triggerBtn.classList.remove("speaking");
        triggerBtn.innerHTML = `<span>🔊 Listen</span>`;
      }
      document.querySelectorAll(".btn-audio-speak.speaking").forEach(btn => {
        btn.classList.remove("speaking");
        btn.innerHTML = `<span>🔊 Listen</span>`;
      });
    };

    utterance.onend = resetUI;
    utterance.onerror = resetUI;

    window.speechSynthesis.speak(utterance);
  }

  function stopSpeech() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    state.isSpeaking = false;
    if (agentVoiceWaveform) agentVoiceWaveform.classList.add("hidden");
    document.querySelectorAll(".btn-audio-speak").forEach(btn => {
      btn.classList.remove("speaking");
      btn.innerHTML = `<span>🔊 Listen</span>`;
    });
  }

  // 5. Speech-to-Text Microphone Integration
  function initSpeechRecognition() {
    if (!voiceMicBtn) return;

    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      voiceMicBtn.addEventListener("click", () => {
        showToast("Voice recognition microphone is not supported in this browser. Please type your question.", "info");
      });
      return;
    }

    const recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    voiceMicBtn.addEventListener("click", () => {
      if (state.isListening) {
        recognition.stop();
        return;
      }

      try {
        recognition.start();
      } catch (err) {
        console.warn("Recognition start error:", err);
      }
    });

    recognition.onstart = () => {
      state.isListening = true;
      voiceMicBtn.classList.add("listening");
      voiceMicBtn.setAttribute("title", "Listening... click to cancel");
      if (chatInputField) {
        chatInputField.placeholder = "🎙️ Listening... speak your plant question now...";
      }
      showToast("🎙️ Listening... speak clearly into your microphone!", "info");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript && transcript.trim()) {
        if (chatInputField) chatInputField.value = transcript.trim();
        sendChatMessage(transcript.trim());
      }
    };

    recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      state.isListening = false;
      voiceMicBtn.classList.remove("listening");
      voiceMicBtn.setAttribute("title", "Click to speak your question with microphone");
      if (chatInputField) {
        chatInputField.placeholder = "Ask anything, or click 🎙️ to speak aloud...";
      }
      if (event.error !== "no-speech" && event.error !== "aborted") {
        showToast(`Microphone error: ${event.error}`, "warning");
      }
    };

    recognition.onend = () => {
      state.isListening = false;
      voiceMicBtn.classList.remove("listening");
      voiceMicBtn.setAttribute("title", "Click to speak your question with microphone");
      if (chatInputField) {
        chatInputField.placeholder = "Ask anything, or click 🎙️ to speak aloud...";
      }
    };
  }

  // 6. Context Management
  function setScanContext(result) {
    state.activeScanContext = {
      disease: formatDisplayName(result.disease),
      crop: formatDisplayName(result.crop),
      disease_id: result.disease_id || result.disease,
      severity: formatDisplayName(result.severity),
      confidence: result.confidence_percentage || `${Math.round((result.confidence || 0.9) * 100)}%`,
      category: formatDisplayName(result.category)
    };

    noContextState.classList.add("hidden");
    activeContextState.classList.remove("hidden");

    ctxDiseaseBadge.textContent = state.activeScanContext.disease;
    ctxCrop.textContent = state.activeScanContext.crop;
    ctxSeverity.textContent = state.activeScanContext.severity;
    ctxConfidence.textContent = state.activeScanContext.confidence;
  }

  function clearContext() {
    state.activeScanContext = null;
    noContextState.classList.remove("hidden");
    activeContextState.classList.add("hidden");
  }

  clearScanContextBtn.addEventListener("click", clearContext);

  clearChatHistoryBtn.addEventListener("click", () => {
    stopSpeech();
    state.chatMessages = [];
    chatMessagesContainer.innerHTML = `
      <div class="chat-message system-agent">
        <div class="msg-avatar">🌿</div>
        <div class="msg-bubble">
          <div class="msg-text">
            Hello! I am your <strong>PlantVision AI Health Agent</strong>. I can speak and converse with you in plain language about your crops, tailored organic remedies, fungicide rotations, and long-term plant care.
            <br><br>
            <em>How can I assist your garden or crops today? You can type below or click 🎙️ to talk!</em>
          </div>
          <div class="msg-audio-actions">
            <button type="button" class="btn-audio-speak" title="Listen to AI voice">
              <span>🔊 Listen</span>
            </button>
          </div>
        </div>
      </div>
    `;
    const initialBtn = chatMessagesContainer.querySelector(".btn-audio-speak");
    if (initialBtn) {
      initialBtn.addEventListener("click", () => {
        const welcomeText = "Hello! I am your PlantVision AI Health Agent. I can speak and converse with you in plain language about your crops, tailored organic remedies, fungicide rotations, and long-term plant care. How can I assist your garden or crops today?";
        speakTextMessage(welcomeText, initialBtn);
      });
    }
    chatSuggestionsBar.innerHTML = "";
  });

  presetWorkflowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const query = btn.getAttribute("data-query");
      if (query) {
        sendChatMessage(query);
      }
    });
  });

  chatInputForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = chatInputField.value.trim();
    if (!query) return;
    chatInputField.value = "";
    sendChatMessage(query);
  });

  function appendChatMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `chat-message ${role === 'user' ? 'user' : 'system-agent'}`;
    
    // Parse markdown-style headers/bold if from assistant
    let formattedText = text;
    if (role === 'assistant') {
      formattedText = text
        .replace(/### (.*?)(<br>|\n|$)/g, '<h4>🌿 $1</h4>')
        .replace(/## (.*?)(<br>|\n|$)/g, '<h3>🌱 $1</h3>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/^\s*[\-\*]\s+(.*)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
    }

    if (role === 'assistant') {
      msgDiv.innerHTML = `
        <div class="msg-avatar">🌿</div>
        <div class="msg-bubble">
          <div class="msg-text">${formattedText}</div>
          <div class="msg-audio-actions">
            <button type="button" class="btn-audio-speak" title="Listen to AI voice">
              <span>🔊 Listen</span>
            </button>
          </div>
        </div>
      `;

      const audioBtn = msgDiv.querySelector(".btn-audio-speak");
      if (audioBtn) {
        audioBtn.addEventListener("click", () => {
          speakTextMessage(text, audioBtn);
        });

        // Auto-play voice speech if enabled
        if (state.voiceAutoPlay) {
          speakTextMessage(text, audioBtn);
        }
      }
    } else {
      msgDiv.innerHTML = `
        <div class="msg-avatar">👤</div>
        <div class="msg-bubble"><div class="msg-text">${formattedText}</div></div>
      `;
    }

    chatMessagesContainer.appendChild(msgDiv);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

    state.chatMessages.push({ role, content: text });
    if (state.chatMessages.length > 25) state.chatMessages.shift();
  }

  function renderSuggestionChips(chips) {
    chatSuggestionsBar.innerHTML = "";
    chips.forEach(chipText => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "suggestion-chip";
      chip.textContent = chipText;
      chip.addEventListener("click", () => sendChatMessage(chipText));
      chatSuggestionsBar.appendChild(chip);
    });
  }

  async function sendChatMessage(query) {
    appendChatMessage("user", query);

    const typingIndicator = document.createElement("div");
    typingIndicator.className = "chat-message system-agent";
    typingIndicator.id = "typing-indicator";
    typingIndicator.innerHTML = `
      <div class="msg-avatar">🌿</div>
      <div class="msg-bubble"><div class="msg-text"><em>AI Agent is formulating agronomic recommendations...</em></div></div>
    `;
    chatMessagesContainer.appendChild(typingIndicator);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          context: state.activeScanContext,
          chat_history: state.chatMessages
        })
      });

      const typingEl = document.getElementById("typing-indicator");
      if (typingEl) typingEl.remove();

      if (!response.ok) throw new Error("Chat request failed.");

      const data = await response.json();
      appendChatMessage("assistant", data.answer);

      if (data.suggested_follow_ups && data.suggested_follow_ups.length) {
        renderSuggestionChips(data.suggested_follow_ups);
      }

    } catch (err) {
      const typingEl = document.getElementById("typing-indicator");
      if (typingEl) typingEl.remove();
      appendChatMessage("assistant", "⚠️ Sorry, I could not process your request at this moment: " + err.message);
    }
  }

  // --------------------------------------------------------------------------
  // DIAGNOSTIC HISTORY LOGS
  // --------------------------------------------------------------------------
  async function loadHistoryLogs() {
    try {
      const headers = {};
      if (state.authToken) {
        headers["Authorization"] = `Bearer ${state.authToken}`;
      }

      const res = await fetch("/history", { headers: headers });
      if (res.ok) {
        const data = await res.json();
        state.history = data.history || [];
        renderHistoryLogs(state.history);
        updateAuthUI();
      }
    } catch (e) {
      console.warn("Could not load history:", e);
    }
  }

  function renderHistoryLogs(items) {
    if (!items.length) {
      historyListWrapper.innerHTML = `<div class="history-empty-msg">No diagnostic records logged yet. Run a scan above to start tracking field health.</div>`;
      return;
    }

    historyListWrapper.innerHTML = "";
    items.forEach(item => {
      const row = document.createElement("div");
      row.className = "history-item-row";
      const cleanDisease = formatDisplayName(item.disease || "Diagnosed Condition");
      const cleanCrop = formatDisplayName(item.crop || "Plant");
      const cleanCategory = item.category || "Pathogen";
      const cleanSeverity = item.severity || "Moderate";

      const sevLower = cleanSeverity.toLowerCase();
      const sevClass = (cleanCategory === "Healthy" || sevLower === "none") ? "severity-healthy" : `severity-${sevLower}`;

      row.innerHTML = `
        <div class="history-item-left">
          <img src="${item.thumbnail || ''}" class="history-thumb" alt="Scan thumbnail">
          <div>
            <div class="history-disease">${cleanDisease}</div>
            <div class="history-meta">${cleanCrop} • ${cleanCategory} • ${item.timestamp || 'Recent'} ${item.user_name && item.user_name !== 'Guest' ? `• By ${item.user_name}` : ''}</div>
          </div>
        </div>
        <div class="history-item-right">
          <span class="severity-pill ${sevClass}">${cleanSeverity}</span>
          <span class="gauge-percent" style="font-size: 0.95rem; color: var(--accent-emerald);">${item.confidence_percentage || '95%'}</span>
        </div>
      `;
      historyListWrapper.appendChild(row);
    });
  }

  clearAllHistoryBtn.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to clear diagnostic history records?")) return;
    try {
      const headers = {};
      if (state.authToken) {
        headers["Authorization"] = `Bearer ${state.authToken}`;
      }
      const res = await fetch("/history", {
        method: "DELETE",
        headers: headers
      });
      if (res.ok) {
        state.history = [];
        renderHistoryLogs([]);
        showToast("Diagnostic history cleared successfully.", "success");
      }
    } catch (e) {
      showToast("Failed to clear history: " + e.message, "error");
    }
  });

});
