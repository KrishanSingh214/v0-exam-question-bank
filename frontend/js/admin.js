// Admin panel module

let adminData = {
    exams: [],
    subjects: [],
    topics: [],
    adminPassword: null,
    statistics: null
};

// Load admin panel
async function loadAdmin() {
    console.log('[v0] Loading admin panel...');
    
    // Prompt for admin password
    const password = prompt('Enter admin password:');
    if (!password) {
        navigateTo('dashboard');
        return;
    }
    
    adminData.adminPassword = password;
    
    try {
        // Load exams
        const exams = await API.getExams();
        adminData.exams = exams;
        populateAdminExamSelect(exams);
        
        // Load statistics
        const stats = await API.getStatistics(password);
        adminData.statistics = stats;
        renderStatistics(stats);
    } catch (error) {
        console.error('[v0] Admin load error:', error);
        showToast('Failed to load admin panel or invalid password', 'error');
        navigateTo('dashboard');
    }
}

// Populate exam select in add question form
function populateAdminExamSelect(exams) {
    const select = document.getElementById('adminExam');
    select.innerHTML = '<option value="">Select Exam</option>';
    
    exams.forEach(exam => {
        const option = document.createElement('option');
        option.value = exam.id;
        option.textContent = exam.name;
        select.appendChild(option);
    });
}

// Load subjects for selected exam in admin
async function loadAdminSubjects() {
    const examId = document.getElementById('adminExam').value;
    
    if (!examId) {
        document.getElementById('adminSubject').innerHTML = '<option value="">Select Subject</option>';
        document.getElementById('adminTopic').innerHTML = '<option value="">Select Topic</option>';
        return;
    }
    
    try {
        const subjects = await API.getSubjects(examId);
        adminData.subjects = subjects;
        
        const select = document.getElementById('adminSubject');
        select.innerHTML = '<option value="">Select Subject</option>';
        
        subjects.forEach(subject => {
            const option = document.createElement('option');
            option.value = subject.id;
            option.textContent = subject.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('[v0] Error loading subjects:', error);
        showToast('Failed to load subjects', 'error');
    }
}

// Load topics for selected subject in admin
async function loadAdminTopics() {
    const subjectId = document.getElementById('adminSubject').value;
    
    if (!subjectId) {
        document.getElementById('adminTopic').innerHTML = '<option value="">Select Topic</option>';
        return;
    }
    
    try {
        const topics = await API.getTopics(subjectId);
        adminData.topics = topics;
        
        const select = document.getElementById('adminTopic');
        select.innerHTML = '<option value="">Select Topic</option>';
        
        topics.forEach(topic => {
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = topic.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('[v0] Error loading topics:', error);
        showToast('Failed to load topics', 'error');
    }
}

// Handle add question form submission
async function handleAddQuestion(event) {
    event.preventDefault();
    console.log('[v0] Adding new question...');
    
    const questionType = document.getElementById('questionType').value;
    const topicId = document.getElementById('adminTopic').value;
    const subjectId = document.getElementById('adminSubject').value;
    const examId = document.getElementById('adminExam').value;
    const questionText = document.getElementById('questionText').value;
    const difficultyLevel = document.getElementById('difficultyLevel').value;
    
    try {
        const questionData = {
            topic_id: parseInt(topicId),
            subject_id: parseInt(subjectId),
            exam_id: parseInt(examId),
            question_text: questionText,
            question_type: questionType,
            difficulty_level: difficultyLevel,
            options: []
        };
        
        // Collect options for MCQ
        if (questionType === 'mcq') {
            const optionInputs = document.querySelectorAll('.option-input');
            if (optionInputs.length === 0) {
                showToast('Please add at least one option for MCQ', 'error');
                return;
            }
            
            optionInputs.forEach(input => {
                questionData.options.push({
                    option_text: input.value,
                    is_correct: input.dataset.correct === 'true'
                });
            });
        }
        
        await API.createQuestion(questionData, adminData.adminPassword);
        showToast('Question added successfully!', 'success');
        document.getElementById('addQuestionForm').reset();
    } catch (error) {
        console.error('[v0] Error adding question:', error);
        showToast('Failed to add question', 'error');
    }
}

// Render statistics
function renderStatistics(stats) {
    const container = document.getElementById('statisticsContent');
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${stats.total_users}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.total_questions}</div>
                <div class="stat-label">Total Questions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.total_attempts}</div>
                <div class="stat-label">Total Attempts</div>
            </div>
        </div>
    `;
}

// Switch admin tabs
function switchAdminTab(tabName) {
    console.log('[v0] Switching admin tab:', tabName);
    
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
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load tab-specific content
    if (tabName === 'statistics' && adminData.statistics) {
        renderStatistics(adminData.statistics);
    }
}

// Export admin functions
window.admin = {
    loadAdmin,
    handleAddQuestion,
    switchAdminTab,
    loadAdminSubjects,
    loadAdminTopics
};
