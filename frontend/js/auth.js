// Authentication module

// Initialize auth forms when page loads
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

// Enhanced login handler with form validation
async function handleLogin(event) {
    event.preventDefault();
    console.log('[v0] Handling login...');
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    // Validation
    if (!username || !password) {
        showToast('Please fill in all fields', 'error');
        return;
    }
    
    try {
        const response = await API.login({ username, password });
        
        // Store authentication data
        localStorage.setItem(CONFIG.TOKEN_KEY, response.access_token);
        localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(response.user));
        
        currentUser = response.user;
        updateNavBar();
        showToast('Login successful!', 'success');
        
        // Clear form
        document.getElementById('loginForm').reset();
        
        // Navigate to dashboard
        setTimeout(() => {
            navigateTo('dashboard');
        }, 500);
    } catch (error) {
        console.error('[v0] Login error:', error);
        showToast(error.message || 'Login failed. Please check your credentials.', 'error');
    }
}

// Enhanced register handler with validation
async function handleRegister(event) {
    event.preventDefault();
    console.log('[v0] Handling registration...');
    
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const username = document.getElementById('regUsername').value.trim();
    const password = document.getElementById('regPassword').value;
    const targetExam = document.getElementById('targetExam').value;
    
    // Validation
    if (!firstName || !lastName || !email || !username || !password || !targetExam) {
        showToast('Please fill in all fields', 'error');
        return;
    }
    
    if (password.length < 6) {
        showToast('Password must be at least 6 characters long', 'error');
        return;
    }
    
    if (!email.includes('@')) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    try {
        const response = await API.register({
            username,
            email,
            password,
            first_name: firstName,
            last_name: lastName,
            target_exam: targetExam
        });
        
        console.log('[v0] Registration successful:', response);
        showToast('Registration successful! Please login with your credentials.', 'success');
        
        // Clear form
        document.getElementById('registerForm').reset();
        
        // Navigate to login after a short delay
        setTimeout(() => {
            navigateTo('login');
        }, 1000);
    } catch (error) {
        console.error('[v0] Registration error:', error);
        
        // Provide specific error messages
        if (error.message.includes('already exists')) {
            showToast('Username or email already exists', 'error');
        } else {
            showToast(error.message || 'Registration failed. Please try again.', 'error');
        }
    }
}

// Logout function
function logout() {
    console.log('[v0] User logging out');
    localStorage.removeItem(CONFIG.TOKEN_KEY);
    localStorage.removeItem(CONFIG.USER_KEY);
    sessionStorage.removeItem('lastPage');
    currentUser = null;
    updateNavBar();
    showToast('You have been logged out', 'info');
    navigateTo('home');
}

// Check if user is authenticated
function isAuthenticated() {
    const token = localStorage.getItem(CONFIG.TOKEN_KEY);
    return !!token && !!currentUser;
}

// Get stored authentication token
function getAuthToken() {
    return localStorage.getItem(CONFIG.TOKEN_KEY);
}

// Get stored user data
function getStoredUser() {
    const userStr = localStorage.getItem(CONFIG.USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
}

// Update current user info from backend
async function refreshUserInfo() {
    try {
        const user = await API.getCurrentUser();
        currentUser = user;
        localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user));
        updateNavBar();
        return user;
    } catch (error) {
        console.error('[v0] Failed to refresh user info:', error);
        throw error;
    }
}

// Export auth functions
window.auth = {
    isAuthenticated,
    getAuthToken,
    getStoredUser,
    refreshUserInfo,
    logout,
    handleLogin,
    handleRegister
};
