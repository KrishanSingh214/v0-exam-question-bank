// Main application logic

let currentPage = 'home';
let currentUser = null;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('[v0] Initializing Question Bank app...');
    
    // Check if user is logged in
    await checkAuthStatus();
    
    // Set initial page
    const storedPage = sessionStorage.getItem('lastPage') || 'home';
    if (currentUser) {
        navigateTo(storedPage === 'home' ? 'dashboard' : storedPage);
    } else {
        navigateTo('home');
    }
});

// Check if user is authenticated
async function checkAuthStatus() {
    const token = localStorage.getItem(CONFIG.TOKEN_KEY);
    const user = localStorage.getItem(CONFIG.USER_KEY);
    
    if (token && user) {
        try {
            const verifyResult = await API.verifyToken();
            if (verifyResult && verifyResult.valid) {
                currentUser = JSON.parse(user);
                updateNavBar();
                console.log('[v0] User authenticated:', currentUser.username);
            } else {
                logout();
            }
        } catch (error) {
            console.error('[v0] Token verification failed:', error);
            logout();
        }
    }
}

// Update navigation bar based on auth status
function updateNavBar() {
    const authNavItems = document.getElementById('authNavItems');
    const guestNavItems = document.getElementById('guestNavItems');
    const userGreeting = document.getElementById('userGreeting');
    
    if (currentUser) {
        authNavItems.style.display = 'flex';
        guestNavItems.style.display = 'none';
        userGreeting.textContent = `Welcome, ${currentUser.first_name}`;
    } else {
        authNavItems.style.display = 'none';
        guestNavItems.style.display = 'flex';
    }
}

// Navigate between pages
function navigateTo(page) {
    console.log('[v0] Navigating to:', page);
    
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    
    // Check if user needs to be authenticated
    if (['dashboard', 'browse', 'admin'].includes(page) && !currentUser) {
        navigateTo('login');
        return;
    }
    
    // Show requested page
    const pageElement = document.getElementById(page);
    if (pageElement) {
        pageElement.classList.add('active');
        currentPage = page;
        sessionStorage.setItem('lastPage', page);
        
        // Load page-specific data
        if (page === 'dashboard') {
            loadDashboard();
        } else if (page === 'browse') {
            loadBrowse();
        } else if (page === 'admin') {
            loadAdmin();
        }
    }
}

// Authentication handlers
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        console.log('[v0] Logging in user:', username);
        const response = await API.login({ username, password });
        
        // Store token and user info
        localStorage.setItem(CONFIG.TOKEN_KEY, response.access_token);
        localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(response.user));
        
        currentUser = response.user;
        updateNavBar();
        showToast('Login successful!', 'success');
        
        // Clear form
        document.getElementById('loginForm').reset();
        
        // Navigate to dashboard
        navigateTo('dashboard');
    } catch (error) {
        handleAPIError(error);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const examInterest = document.getElementById('targetExam').value;
    
    try {
        console.log('[v0] Registering new user:', username);
        const response = await API.register({
            username,
            email,
            password,
            full_name: `${firstName} ${lastName}`,
            exam_interest: examInterest
        });
        
        // Store token and user info
        localStorage.setItem(CONFIG.TOKEN_KEY, response.access_token);
        
        showToast('Registration successful! Logged in.', 'success');
        document.getElementById('registerForm').reset();
        
        // Get current user info and navigate
        const user = await API.getCurrentUser();
        currentUser = user;
        updateNavBar();
        navigateTo('dashboard');
    } catch (error) {
        handleAPIError(error);
    }
}

function logout() {
    console.log('[v0] Logging out user');
    localStorage.removeItem(CONFIG.TOKEN_KEY);
    localStorage.removeItem(CONFIG.USER_KEY);
    currentUser = null;
    updateNavBar();
    showToast('Logged out successfully', 'info');
    navigateTo('home');
}

// Tab switching for admin panel
function switchAdminTab(tabName) {
    console.log('[v0] Switching to admin tab:', tabName);
    
    // Hide all tabs
    document.querySelectorAll('.admin-tab-content').forEach(tab => {
        tab.classList.remove('active');
        tab.classList.add('hidden');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show requested tab
    const tabElement = document.getElementById(`${tabName}-tab`);
    if (tabElement) {
        tabElement.classList.remove('hidden');
        tabElement.classList.add('active');
    }
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function getDifficultyClass(difficulty) {
    const lower = difficulty.toLowerCase();
    if (lower === 'easy') return 'difficulty-easy';
    if (lower === 'medium') return 'difficulty-medium';
    if (lower === 'hard') return 'difficulty-hard';
    return 'difficulty-easy';
}

function getDifficultyLabel(difficulty) {
    const lower = difficulty.toLowerCase();
    return lower.charAt(0).toUpperCase() + lower.slice(1);
}

// Placeholder functions for page-specific loading (will be implemented in separate files)
function loadDashboard() {
    console.log('[v0] Loading dashboard...');
}

function loadBrowse() {
    console.log('[v0] Loading browse page...');
}

function loadAdmin() {
    console.log('[v0] Loading admin panel...');
}

// Export for use in other modules
window.app = {
    navigateTo,
    handleLogin,
    handleRegister,
    logout,
    switchAdminTab,
    currentUser,
    showToast,
    formatDate,
    getDifficultyClass
};
