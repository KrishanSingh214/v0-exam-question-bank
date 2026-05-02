// ==================== Configuration ====================
const API_BASE_URL = 'http://localhost:8000/api';
const STORAGE_KEY = 'qb_user';
const TOKEN_KEY = 'qb_token';

let currentUser = null;
let currentQuestion = null;
let allExams = [];
let allSubjects = [];
let allTopics = [];
let allQuestions = [];
let currentQuestionIndex = 0;

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', () => {
    console.log("[v0] Initializing Question Bank application");
    loadUserSession();
    loadExams();
});

// ==================== Auth Functions ====================
function showLoginModal() {
    if (currentUser) return;
    document.getElementById('loginModal').classList.add('show');
}

function closeLoginModal() {
    document.getElementById('loginModal').classList.remove('show');
}

function showRegisterModal() {
    document.getElementById('registerModal').classList.add('show');
}

function closeRegisterModal() {
    document.getElementById('registerModal').classList.remove('show');
}

function switchToRegister() {
    closeLoginModal();
    showRegisterModal();
}

function switchToLogin() {
    closeRegisterModal();
    showLoginModal();
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        currentUser = data.user;
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(currentUser));

        closeLoginModal();
        updateAuthUI();
        showToast('Login successful!', 'success');
        navigateTo('dashboard');
        loadUserProgress();
    } catch (error) {
        console.error('[v0] Login error:', error);
        showToast('Login failed. Please try again.', 'error');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const fullName = document.getElementById('registerFullName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const targetExam = document.getElementById('registerExam').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username,
                email,
                password,
                full_name: fullName,
                target_exam: targetExam
            })
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        const data = await response.json();
        currentUser = data.user;
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(currentUser));

        closeRegisterModal();
        updateAuthUI();
        showToast('Registration successful!', 'success');
        navigateTo('dashboard');
        loadUserProgress();
    } catch (error) {
        console.error('[v0] Register error:', error);
        showToast('Registration failed. Please try again.', 'error');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(STORAGE_KEY);
    updateAuthUI();
    showToast('Logged out successfully', 'success');
    navigateTo('home');
}

function loadUserSession() {
    const userJson = localStorage.getItem(STORAGE_KEY);
    if (userJson) {
        currentUser = JSON.parse(userJson);
        updateAuthUI();
        console.log('[v0] User session loaded:', currentUser);
    }
}

function updateAuthUI() {
    const authMenu = document.getElementById('authMenu');
    const userMenu = document.getElementById('userMenu');

    if (currentUser) {
        authMenu.style.display = 'none';
        userMenu.style.display = 'flex';
        document.getElementById('userGreeting').textContent = `Hi, ${currentUser.full_name}`;
    } else {
        authMenu.style.display = 'block';
        userMenu.style.display = 'none';
    }
}

// ==================== Navigation ====================
function navigateTo(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    const selectedPage = document.getElementById(pageId);
    if (selectedPage) {
        selectedPage.classList.add('active');
    }

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');

    // Load page content
    if (pageId === 'dashboard' && currentUser) {
        loadUserProgress();
        loadRecommendations();
    } else if (pageId === 'browse') {
        loadQuestions();
    } else if (pageId === 'bookmarks' && currentUser) {
        loadBookmarks();
    }
}

// ==================== Data Loading ====================
async function loadExams() {
    try {
        const response = await fetch(`${API_BASE_URL}/exams`);
        const data = await response.json();
        allExams = data;

        const examFilter = document.getElementById('examFilter');
        examFilter.innerHTML = '<option value="">All Exams</option>';
        data.forEach(exam => {
            const option = document.createElement('option');
            option.value = exam.id;
            option.textContent = exam.name;
            examFilter.appendChild(option);
        });

        console.log('[v0] Exams loaded:', data.length);
    } catch (error) {
        console.error('[v0] Error loading exams:', error);
    }
}

async function loadSubjects() {
    const examId = document.getElementById('examFilter').value;
    if (!examId) {
        document.getElementById('subjectFilter').innerHTML = '<option value="">All Subjects</option>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/exams/${examId}/subjects`);
        const data = await response.json();
        allSubjects = data;

        const subjectFilter = document.getElementById('subjectFilter');
        subjectFilter.innerHTML = '<option value="">All Subjects</option>';
        data.forEach(subject => {
            const option = document.createElement('option');
            option.value = subject.id;
            option.textContent = subject.name;
            subjectFilter.appendChild(option);
        });

        console.log('[v0] Subjects loaded:', data.length);
    } catch (error) {
        console.error('[v0] Error loading subjects:', error);
    }
}

async function loadTopics() {
    const subjectId = document.getElementById('subjectFilter').value;
    if (!subjectId) {
        document.getElementById('topicFilter').innerHTML = '<option value="">All Topics</option>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/subjects/${subjectId}/topics`);
        const data = await response.json();
        allTopics = data;

        const topicFilter = document.getElementById('topicFilter');
        topicFilter.innerHTML = '<option value="">All Topics</option>';
        data.forEach(topic => {
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = topic.name;
            topicFilter.appendChild(option);
        });

        console.log('[v0] Topics loaded:', data.length);
    } catch (error) {
        console.error('[v0] Error loading topics:', error);
    }
}

async function loadQuestions() {
    const topicId = document.getElementById('topicFilter').value;
    const difficulty = document.getElementById('difficultyFilter').value;
    const searchTerm = document.getElementById('searchFilter').value.toLowerCase();

    try {
        let url = `${API_BASE_URL}/questions?skip=0&limit=100`;
        if (topicId) url += `&topic_id=${topicId}`;
        if (difficulty) url += `&difficulty=${difficulty}`;

        const response = await fetch(url);
        let data = await response.json();

        // Filter by search term on client side
        if (searchTerm) {
            data = data.filter(q => 
                q.question_text.toLowerCase().includes(searchTerm)
            );
        }

        allQuestions = data;
        displayQuestions(data);
        console.log('[v0] Questions loaded:', data.length);
    } catch (error) {
        console.error('[v0] Error loading questions:', error);
        showToast('Error loading questions', 'error');
    }
}

function displayQuestions(questions) {
    const questionsList = document.getElementById('questionsList');
    
    if (questions.length === 0) {
        questionsList.innerHTML = '<p class="loading">No questions found</p>';
        return;
    }

    questionsList.innerHTML = questions.map(q => `
        <div class="question-card" onclick="viewQuestion(${q.id})">
            <h4>${q.question_text.substring(0, 100)}...</h4>
            <div class="question-meta">
                <span class="difficulty-badge ${q.difficulty_level.toLowerCase()}">${q.difficulty_level}</span>
                <span class="question-topic">${q.question_type || 'Multiple Choice'}</span>
            </div>
        </div>
    `).join('');
}

async function viewQuestion(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/questions/${questionId}`);
        const question = await response.json();
        currentQuestion = question;

        // Display question detail
        navigateTo('questionDetail');
        displayQuestionDetail(question);
        console.log('[v0] Question loaded:', question.id);
    } catch (error) {
        console.error('[v0] Error loading question detail:', error);
        showToast('Error loading question', 'error');
    }
}

function displayQuestionDetail(question) {
    document.getElementById('detailQuestion').textContent = question.question_text;
    
    const difficultyClass = question.difficulty_level.toLowerCase();
    document.getElementById('detailDifficulty').textContent = question.difficulty_level;
    document.getElementById('detailDifficulty').className = `difficulty-badge ${difficultyClass}`;

    const optionsList = document.getElementById('detailOptions');
    optionsList.innerHTML = question.options.map(option => `
        <div class="option" onclick="selectOption('${option.option_label}')">
            <input type="radio" name="answer" value="${option.option_label}">
            <label><strong>${option.option_label}.</strong> ${option.option_text}</label>
        </div>
    `).join('');

    // Hide result initially
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('submitBtn').style.display = 'block';
}

function selectOption(label) {
    document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    const radio = event.currentTarget.querySelector('input[type="radio"]');
    radio.checked = true;
}

async function submitAnswer() {
    if (!currentUser) {
        showToast('Please login to submit answers', 'error');
        return;
    }

    const selectedAnswer = document.querySelector('input[name="answer"]:checked');
    if (!selectedAnswer) {
        showToast('Please select an option', 'error');
        return;
    }

    try {
        const token = localStorage.getItem(TOKEN_KEY);
        const response = await fetch(`${API_BASE_URL}/progress/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                question_id: currentQuestion.id,
                answer: selectedAnswer.value,
                time_spent: 30
            })
        });

        const result = await response.json();
        
        // Show result
        document.getElementById('submitBtn').style.display = 'none';
        const resultContainer = document.getElementById('resultContainer');
        resultContainer.style.display = 'block';

        const resultMessage = document.getElementById('resultMessage');
        const correctOption = currentQuestion.options.find(o => o.is_correct);
        
        if (result.is_correct) {
            resultMessage.textContent = '✓ Correct!';
            resultMessage.className = 'result-message correct';
        } else {
            resultMessage.textContent = `✗ Incorrect. The correct answer is ${correctOption.option_label}`;
            resultMessage.className = 'result-message incorrect';
        }

        const explanation = document.getElementById('explanation');
        explanation.innerHTML = `<strong>Explanation:</strong> ${currentQuestion.explanation || 'No explanation available'}`;

        console.log('[v0] Answer submitted:', result);
    } catch (error) {
        console.error('[v0] Error submitting answer:', error);
        showToast('Error submitting answer', 'error');
    }
}

async function loadUserProgress() {
    if (!currentUser) {
        showToast('Please login to view progress', 'error');
        return;
    }

    try {
        const token = localStorage.getItem(TOKEN_KEY);
        const response = await fetch(`${API_BASE_URL}/progress/user`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const progress = await response.json();
        
        document.getElementById('attemptedCount').textContent = progress.total_questions_attempted;
        document.getElementById('correctCount').textContent = progress.correct_answers;
        document.getElementById('accuracyRate').textContent = progress.accuracy_percentage.toFixed(1) + '%';
        document.getElementById('weakTopicsCount').textContent = Math.ceil(progress.total_questions_attempted / 5);

        console.log('[v0] User progress loaded:', progress);
    } catch (error) {
        console.error('[v0] Error loading user progress:', error);
    }
}

async function loadRecommendations() {
    if (!currentUser) return;

    try {
        const token = localStorage.getItem(TOKEN_KEY);
        const response = await fetch(`${API_BASE_URL}/recommendations?limit=5`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const recommendations = await response.json();
        
        const recommendedList = document.getElementById('recommendedList');
        if (recommendations.length === 0) {
            recommendedList.innerHTML = '<p class="loading">No recommendations yet. Keep practicing!</p>';
        } else {
            recommendedList.innerHTML = recommendations.map(q => `
                <div class="question-card" onclick="viewQuestion(${q.id})">
                    <h4>${q.question_text.substring(0, 80)}...</h4>
                    <div class="question-meta">
                        <span class="difficulty-badge ${q.difficulty_level.toLowerCase()}">${q.difficulty_level}</span>
                    </div>
                </div>
            `).join('');
        }

        console.log('[v0] Recommendations loaded:', recommendations.length);
    } catch (error) {
        console.error('[v0] Error loading recommendations:', error);
    }
}

async function loadBookmarks() {
    if (!currentUser) {
        showToast('Please login to view bookmarks', 'error');
        return;
    }

    try {
        const token = localStorage.getItem(TOKEN_KEY);
        const response = await fetch(`${API_BASE_URL}/bookmarks`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const bookmarks = await response.json();
        
        const bookmarksList = document.getElementById('bookmarksList');
        if (bookmarks.length === 0) {
            bookmarksList.innerHTML = '<p class="loading">No bookmarks yet</p>';
        } else {
            bookmarksList.innerHTML = bookmarks.map(q => `
                <div class="question-card" onclick="viewQuestion(${q.id})">
                    <h4>${q.question_text.substring(0, 100)}...</h4>
                    <div class="question-meta">
                        <span class="difficulty-badge ${q.difficulty_level.toLowerCase()}">${q.difficulty_level}</span>
                    </div>
                </div>
            `).join('');
        }

        console.log('[v0] Bookmarks loaded:', bookmarks.length);
    } catch (error) {
        console.error('[v0] Error loading bookmarks:', error);
    }
}

async function toggleBookmark() {
    if (!currentUser) {
        showToast('Please login to bookmark', 'error');
        return;
    }

    try {
        const token = localStorage.getItem(TOKEN_KEY);
        const response = await fetch(`${API_BASE_URL}/bookmarks/${currentQuestion.id}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            showToast('Question bookmarked!', 'success');
        }
    } catch (error) {
        console.error('[v0] Error bookmarking question:', error);
        showToast('Error bookmarking question', 'error');
    }
}

// ==================== UI Utilities ====================
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Close modals when clicking outside
window.onclick = function(event) {
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    
    if (event.target === loginModal) {
        closeLoginModal();
    }
    if (event.target === registerModal) {
        closeRegisterModal();
    }
};

console.log('[v0] Question Bank application loaded successfully');
