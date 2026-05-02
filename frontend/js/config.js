// Configuration file for the Question Bank application

const CONFIG = {
    // Backend API base URL
    API_BASE_URL: 'http://localhost:8000/api',
    
    // Admin password (for admin panel)
    ADMIN_PASSWORD: 'admin123',
    
    // Pagination
    ITEMS_PER_PAGE: 12,
    
    // Token storage key
    TOKEN_KEY: 'qb_token',
    USER_KEY: 'qb_user',
    
    // API Endpoints
    ENDPOINTS: {
        // Auth
        REGISTER: '/auth/register',
        LOGIN: '/auth/login',
        VERIFY_TOKEN: '/auth/verify-token',
        GET_CURRENT_USER: '/auth/me',
        
        // Questions
        GET_QUESTIONS: '/questions',
        GET_QUESTION_DETAIL: '/questions/:id',
        SEARCH_QUESTIONS: '/questions/search/advanced',
        GET_BOOKMARKS: '/questions/bookmarks/user',
        ADD_BOOKMARK: '/questions/bookmarks',
        REMOVE_BOOKMARK: '/questions/bookmarks/:id',
        
        // User Progress
        RECORD_PROGRESS: '/users/progress',
        GET_USER_STATS: '/users/stats',
        GET_PROGRESS: '/users/progress/:id',
        GET_HISTORY: '/users/history',
        
        // Recommendations
        GET_RECOMMENDATIONS: '/recommendations/personalized',
        GET_TOPIC_RECOMMENDATIONS: '/recommendations/by-topic/:id',
        GET_DIFFICULTY_PROGRESSION: '/recommendations/difficulty-progression',
        RETRAIN_MODEL: '/recommendations/retrain',
        
        // Admin
        CREATE_EXAM: '/admin/exams',
        GET_EXAMS: '/admin/exams',
        CREATE_SUBJECT: '/admin/subjects',
        GET_SUBJECTS: '/admin/subjects',
        CREATE_TOPIC: '/admin/topics',
        GET_TOPICS: '/admin/topics',
        CREATE_QUESTION: '/admin/questions',
        UPDATE_QUESTION: '/admin/questions/:id',
        DELETE_QUESTION: '/admin/questions/:id',
        GET_STATISTICS: '/admin/statistics'
    }
};

// Utility function to get full API URL
function getApiUrl(endpoint, params = {}) {
    let url = CONFIG.API_BASE_URL + endpoint;
    
    // Replace path parameters
    for (const [key, value] of Object.entries(params)) {
        url = url.replace(`:${key}`, value);
    }
    
    return url;
}
