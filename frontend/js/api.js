// API wrapper for making requests to the backend

class API {
    static getAuthHeaders() {
        const token = localStorage.getItem(CONFIG.TOKEN_KEY);
        return {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    }

    static async request(method, endpoint, data = null, params = {}) {
        const url = new URL(getApiUrl(endpoint, params));
        
        const options = {
            method,
            headers: this.getAuthHeaders(),
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url.toString(), options);
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`[v0] API Error:`, error);
            throw error;
        }
    }

    // Authentication
    static async register(userData) {
        return this.request('POST', CONFIG.ENDPOINTS.REGISTER, userData);
    }

    static async login(credentials) {
        return this.request('POST', CONFIG.ENDPOINTS.LOGIN, credentials);
    }

    static async verifyToken() {
        const token = localStorage.getItem(CONFIG.TOKEN_KEY);
        if (!token) return null;
        try {
            return await this.request('POST', CONFIG.ENDPOINTS.VERIFY_TOKEN);
        } catch {
            return null;
        }
    }

    static async getCurrentUser() {
        return this.request('GET', CONFIG.ENDPOINTS.GET_CURRENT_USER);
    }

    // Questions
    static async getQuestions(filters = {}) {
        const queryString = new URLSearchParams(filters).toString();
        const endpoint = `${CONFIG.ENDPOINTS.GET_QUESTIONS}?${queryString}`;
        return this.request('GET', endpoint);
    }

    static async getQuestionDetail(questionId) {
        return this.request('GET', CONFIG.ENDPOINTS.GET_QUESTION_DETAIL, null, { id: questionId });
    }

    static async searchQuestions(searchParams) {
        return this.request('GET', CONFIG.ENDPOINTS.SEARCH_QUESTIONS, null, searchParams);
    }

    // Bookmarks
    static async getBookmarks() {
        return this.request('GET', CONFIG.ENDPOINTS.GET_BOOKMARKS);
    }

    static async addBookmark(questionId) {
        return this.request('POST', CONFIG.ENDPOINTS.ADD_BOOKMARK, { question_id: questionId });
    }

    static async removeBookmark(questionId) {
        return this.request('DELETE', CONFIG.ENDPOINTS.REMOVE_BOOKMARK, null, { id: questionId });
    }

    // User Progress
    static async recordProgress(questionId, isCorrect, timeSpent = null) {
        return this.request('POST', CONFIG.ENDPOINTS.RECORD_PROGRESS, {
            question_id: questionId,
            is_correct: isCorrect,
            time_spent_seconds: timeSpent
        });
    }

    static async getUserStats() {
        return this.request('GET', CONFIG.ENDPOINTS.GET_USER_STATS);
    }

    static async getQuestionProgress(questionId) {
        return this.request('GET', CONFIG.ENDPOINTS.GET_PROGRESS, null, { id: questionId });
    }

    static async getHistory(limit = 50) {
        return this.request('GET', `${CONFIG.ENDPOINTS.GET_HISTORY}?limit=${limit}`);
    }

    // Recommendations
    static async getRecommendations(limit = 10) {
        return this.request('GET', `${CONFIG.ENDPOINTS.GET_RECOMMENDATIONS}?limit=${limit}`);
    }

    static async getTopicRecommendations(topicId, limit = 10) {
        return this.request('GET', CONFIG.ENDPOINTS.GET_TOPIC_RECOMMENDATIONS, null, { id: topicId, limit });
    }

    static async getDifficultyProgression(subjectId = null) {
        const params = subjectId ? { subject_id: subjectId } : {};
        return this.request('GET', CONFIG.ENDPOINTS.GET_DIFFICULTY_PROGRESSION, null, params);
    }

    static async retrainModel() {
        return this.request('POST', CONFIG.ENDPOINTS.RETRAIN_MODEL);
    }

    // Admin - Exams
    static async createExam(examData, adminPassword) {
        return this.request('POST', `${CONFIG.ENDPOINTS.CREATE_EXAM}?admin_password=${adminPassword}`, examData);
    }

    static async getExams() {
        return this.request('GET', CONFIG.ENDPOINTS.GET_EXAMS);
    }

    // Admin - Subjects
    static async createSubject(subjectData, adminPassword) {
        return this.request('POST', `${CONFIG.ENDPOINTS.CREATE_SUBJECT}?admin_password=${adminPassword}`, subjectData);
    }

    static async getSubjects(examId = null) {
        const params = examId ? `?exam_id=${examId}` : '';
        return this.request('GET', `${CONFIG.ENDPOINTS.GET_SUBJECTS}${params}`);
    }

    // Admin - Topics
    static async createTopic(topicData, adminPassword) {
        return this.request('POST', `${CONFIG.ENDPOINTS.CREATE_TOPIC}?admin_password=${adminPassword}`, topicData);
    }

    static async getTopics(subjectId = null) {
        const params = subjectId ? `?subject_id=${subjectId}` : '';
        return this.request('GET', `${CONFIG.ENDPOINTS.GET_TOPICS}${params}`);
    }

    // Admin - Questions
    static async createQuestion(questionData, adminPassword) {
        return this.request('POST', `${CONFIG.ENDPOINTS.CREATE_QUESTION}?admin_password=${adminPassword}`, questionData);
    }

    static async updateQuestion(questionId, questionData, adminPassword) {
        return this.request('PUT', `${CONFIG.ENDPOINTS.UPDATE_QUESTION}?admin_password=${adminPassword}`, questionData, { id: questionId });
    }

    static async deleteQuestion(questionId, adminPassword) {
        return this.request('DELETE', `${CONFIG.ENDPOINTS.DELETE_QUESTION}?admin_password=${adminPassword}`, null, { id: questionId });
    }

    static async getStatistics(adminPassword) {
        return this.request('GET', `${CONFIG.ENDPOINTS.GET_STATISTICS}?admin_password=${adminPassword}`);
    }
}

// Helper function to show toast messages
function showToast(message, type = 'success', duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// Helper function to handle API errors
function handleAPIError(error) {
    console.error('[v0] API Error:', error);
    const message = error.message || 'An error occurred. Please try again.';
    showToast(message, 'error');
}
