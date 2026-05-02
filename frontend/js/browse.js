// Browse questions module

let browseData = {
    questions: [],
    exams: [],
    subjects: [],
    topics: [],
    currentPage: 0,
    totalPages: 0,
    filters: {
        exam_id: null,
        subject_id: null,
        topic_id: null,
        difficulty_level: null,
        keyword: null
    }
};

// Load browse page
async function loadBrowse() {
    console.log('[v0] Loading browse page...');
    
    try {
        // Load exams for filter
        const exams = await API.getExams();
        browseData.exams = exams;
        populateExamFilter(exams);
        
        // Load initial questions
        await applyFilters();
    } catch (error) {
        console.error('[v0] Browse load error:', error);
        showToast('Failed to load browse page', 'error');
    }
}

// Populate exam dropdown
function populateExamFilter(exams) {
    const select = document.getElementById('filterExam');
    select.innerHTML = '<option value="">All Exams</option>';
    
    exams.forEach(exam => {
        const option = document.createElement('option');
        option.value = exam.id;
        option.textContent = exam.name;
        select.appendChild(option);
    });
}

// Load subjects for selected exam
async function loadSubjectsForExam() {
    const examId = document.getElementById('filterExam').value;
    
    if (!examId) {
        document.getElementById('filterSubject').innerHTML = '<option value="">All Subjects</option>';
        document.getElementById('filterTopic').innerHTML = '<option value="">All Topics</option>';
        return;
    }
    
    try {
        const subjects = await API.getSubjects(examId);
        browseData.subjects = subjects;
        
        const select = document.getElementById('filterSubject');
        select.innerHTML = '<option value="">All Subjects</option>';
        
        subjects.forEach(subject => {
            const option = document.createElement('option');
            option.value = subject.id;
            option.textContent = subject.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('[v0] Error loading subjects:', error);
    }
}

// Load topics for selected subject
async function loadTopicsForSubject() {
    const subjectId = document.getElementById('filterSubject').value;
    
    if (!subjectId) {
        document.getElementById('filterTopic').innerHTML = '<option value="">All Topics</option>';
        return;
    }
    
    try {
        const topics = await API.getTopics(subjectId);
        browseData.topics = topics;
        
        const select = document.getElementById('filterTopic');
        select.innerHTML = '<option value="">All Topics</option>';
        
        topics.forEach(topic => {
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = topic.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('[v0] Error loading topics:', error);
    }
}

// Apply filters and load questions
async function applyFilters() {
    console.log('[v0] Applying filters...');
    
    browseData.filters = {
        exam_id: document.getElementById('filterExam').value || null,
        subject_id: document.getElementById('filterSubject').value || null,
        topic_id: document.getElementById('filterTopic').value || null,
        difficulty_level: document.getElementById('filterDifficulty').value || null,
        keyword: document.getElementById('searchKeyword').value || null
    };
    
    browseData.currentPage = 0;
    
    try {
        // Build query params
        const params = {
            limit: CONFIG.ITEMS_PER_PAGE,
            offset: 0
        };
        
        Object.entries(browseData.filters).forEach(([key, value]) => {
            if (value) params[key] = value;
        });
        
        const questions = await API.getQuestions(params);
        browseData.questions = questions;
        browseData.totalPages = Math.ceil(questions.length / CONFIG.ITEMS_PER_PAGE);
        
        renderQuestions();
    } catch (error) {
        console.error('[v0] Filter error:', error);
        showToast('Failed to load questions', 'error');
    }
}

// Render questions list
function renderQuestions() {
    const container = document.getElementById('questionsList');
    container.innerHTML = '';
    
    if (browseData.questions.length === 0) {
        container.innerHTML = '<p class="loading">No questions found. Try adjusting your filters.</p>';
        renderPagination();
        return;
    }
    
    const start = browseData.currentPage * CONFIG.ITEMS_PER_PAGE;
    const end = start + CONFIG.ITEMS_PER_PAGE;
    const pageQuestions = browseData.questions.slice(start, end);
    
    pageQuestions.forEach(question => {
        const card = document.createElement('div');
        card.className = 'question-card';
        card.onclick = () => viewQuestionDetail(question.id);
        
        card.innerHTML = `
            <h3>${question.question_text.substring(0, 100)}...</h3>
            <div class="question-meta">
                <span class="difficulty-badge ${getDifficultyClass(question.difficulty_level)}">
                    ${getDifficultyLabel(question.difficulty_level)}
                </span>
            </div>
        `;
        container.appendChild(card);
    });
    
    renderPagination();
}

// Render pagination
function renderPagination() {
    const container = document.getElementById('pagination');
    container.innerHTML = '';
    
    if (browseData.totalPages <= 1) return;
    
    for (let i = 0; i < browseData.totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i + 1;
        btn.className = i === browseData.currentPage ? 'active' : '';
        btn.onclick = () => {
            browseData.currentPage = i;
            renderQuestions();
        };
        container.appendChild(btn);
    }
}

// View question detail
async function viewQuestionDetail(questionId) {
    console.log('[v0] Loading question detail:', questionId);
    
    try {
        const question = await API.getQuestionDetail(questionId);
        const progress = await API.getQuestionProgress(questionId);
        
        // Store question data
        sessionStorage.setItem('currentQuestion', JSON.stringify({ question, progress }));
        
        // Render detail view
        renderQuestionDetail(question, progress);
        
        // Navigate to detail page
        navigateTo('questionDetail');
    } catch (error) {
        console.error('[v0] Error loading question:', error);
        showToast('Failed to load question details', 'error');
    }
}

// Render question detail
function renderQuestionDetail(question, progress) {
    const container = document.getElementById('questionContent');
    container.innerHTML = '';
    
    const detailCard = document.createElement('div');
    detailCard.className = 'question-detail-container';
    
    let optionsHtml = '';
    if (question.options && question.options.length > 0) {
        optionsHtml = '<div class="options-list">';
        question.options.forEach((option, index) => {
            optionsHtml += `
                <div class="option-item">
                    <input type="radio" id="option${index}" name="answer" value="${index}">
                    <label for="option${index}">${option.option_text}</label>
                </div>
            `;
        });
        optionsHtml += '</div>';
    }
    
    detailCard.innerHTML = `
        <div class="question-detail-header">
            <h2>${question.question_text}</h2>
            <div class="question-meta">
                <span class="difficulty-badge ${getDifficultyClass(question.difficulty_level)}">
                    ${getDifficultyLabel(question.difficulty_level)}
                </span>
            </div>
        </div>
        
        ${optionsHtml}
        
        <div class="question-actions">
            <button class="btn btn-primary" onclick="submitAnswer('${question.id}')">Submit Answer</button>
            <button class="btn btn-secondary" onclick="toggleBookmark('${question.id}')">Bookmark</button>
        </div>
        
        <div id="result" style="display:none;" class="result-section"></div>
    `;
    
    container.appendChild(detailCard);
}

// Submit answer
async function submitAnswer(questionId) {
    const selected = document.querySelector('input[name="answer"]:checked');
    
    if (!selected) {
        showToast('Please select an answer', 'error');
        return;
    }
    
    try {
        const questionData = JSON.parse(sessionStorage.getItem('currentQuestion'));
        const selectedIndex = parseInt(selected.value);
        const correctOption = questionData.question.options.find(opt => opt.is_correct);
        const isCorrect = questionData.question.options[selectedIndex].is_correct;
        
        // Record progress
        await API.recordProgress(questionId, isCorrect);
        
        // Show result
        const resultDiv = document.getElementById('result');
        resultDiv.style.display = 'block';
        resultDiv.className = isCorrect ? 'correct' : 'incorrect';
        resultDiv.innerHTML = `
            <p>${isCorrect ? 'Correct!' : 'Incorrect!'}</p>
            <p>The correct answer is: ${correctOption.option_text}</p>
        `;
        
        showToast(isCorrect ? 'Correct answer!' : 'Incorrect answer', isCorrect ? 'success' : 'error');
    } catch (error) {
        console.error('[v0] Error submitting answer:', error);
        showToast('Failed to record answer', 'error');
    }
}

// Toggle bookmark
async function toggleBookmark(questionId) {
    try {
        const btn = event.target;
        
        // Check if already bookmarked
        const bookmarks = await API.getBookmarks();
        const isBookmarked = bookmarks.some(b => b.id === questionId);
        
        if (isBookmarked) {
            await API.removeBookmark(questionId);
            showToast('Bookmark removed', 'info');
            btn.textContent = 'Bookmark';
        } else {
            await API.addBookmark(questionId);
            showToast('Question bookmarked!', 'success');
            btn.textContent = 'Unbookmark';
        }
    } catch (error) {
        console.error('[v0] Error toggling bookmark:', error);
        showToast('Failed to update bookmark', 'error');
    }
}

// Export browse functions
window.browse = {
    loadBrowse,
    applyFilters,
    viewQuestionDetail,
    submitAnswer,
    toggleBookmark,
    loadSubjectsForExam,
    loadTopicsForSubject
};
