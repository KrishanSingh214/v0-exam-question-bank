// Dashboard module

let dashboardData = {
    stats: null,
    recommendations: [],
    weakTopics: []
};

// Load dashboard data
async function loadDashboard() {
    console.log('[v0] Loading dashboard...');
    
    try {
        // Load user stats
        const stats = await API.getUserStats();
        dashboardData.stats = stats;
        
        // Load recommendations
        const recommendations = await API.getRecommendations(10);
        dashboardData.recommendations = recommendations;
        
        // Render dashboard
        renderDashboard();
    } catch (error) {
        console.error('[v0] Dashboard load error:', error);
        showToast('Failed to load dashboard', 'error');
    }
}

// Render dashboard content
function renderDashboard() {
    const stats = dashboardData.stats;
    
    // Update stats
    document.getElementById('totalAttempted').textContent = stats.total_attempted;
    document.getElementById('correctAnswers').textContent = stats.total_correct;
    document.getElementById('accuracy').textContent = Math.round(stats.accuracy_percentage) + '%';
    
    // Render weak topics
    renderWeakTopics(stats.weak_topics);
    
    // Render recommendations
    renderRecommendations(dashboardData.recommendations);
}

// Render weak topics section
function renderWeakTopics(weakTopics) {
    const container = document.getElementById('weakTopicsList');
    container.innerHTML = '';
    
    if (!weakTopics || weakTopics.length === 0) {
        container.innerHTML = '<p class="loading">Great job! No weak areas detected.</p>';
        return;
    }
    
    weakTopics.forEach(topic => {
        const card = document.createElement('div');
        card.className = 'weak-topic-card';
        card.innerHTML = `
            <h4>${topic.topic_name}</h4>
            <div class="weak-topic-stats">
                <p>Accuracy: ${Math.round(topic.accuracy_percentage)}%</p>
                <p>Attempted: ${topic.attempted} questions</p>
                <p>Correct: ${topic.correct} answers</p>
                <button class="btn btn-primary" onclick="navigateToTopicQuestions(${topic.topic_id})">
                    Practice This Topic
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Render recommendations section
function renderRecommendations(recommendations) {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p class="loading">No recommendations available yet. Practice some questions first!</p>';
        return;
    }
    
    recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'question-card';
        card.onclick = () => viewQuestionDetail(rec.question_id);
        
        card.innerHTML = `
            <h3>${rec.question_text}</h3>
            <div class="question-meta">
                <span class="difficulty-badge ${getDifficultyClass(rec.difficulty_level)}">
                    ${getDifficultyLabel(rec.difficulty_level)}
                </span>
                <span class="topic-badge">${rec.weak_topic}</span>
            </div>
            <p style="font-size: 0.875rem; color: var(--neutral-700);">
                ${rec.reason}
            </p>
        `;
        container.appendChild(card);
    });
}

// Navigate to view weak topic questions
async function navigateToTopicQuestions(topicId) {
    console.log('[v0] Loading questions for weak topic:', topicId);
    
    try {
        const questions = await API.getTopicRecommendations(topicId, 20);
        
        // Store in session and navigate to browse
        sessionStorage.setItem('filteredQuestions', JSON.stringify(questions));
        sessionStorage.setItem('selectedTopicId', topicId);
        
        navigateTo('browse');
        // Note: loadBrowse() will need to check for this stored data
    } catch (error) {
        console.error('[v0] Error loading topic questions:', error);
        showToast('Failed to load questions for this topic', 'error');
    }
}

// Export dashboard functions
window.dashboard = {
    loadDashboard,
    navigateToTopicQuestions
};
