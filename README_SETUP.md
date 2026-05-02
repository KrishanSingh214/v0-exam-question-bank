# Question Bank - Setup & Deployment Guide

## Project Overview

**Question Bank** is an AI-powered exam preparation platform featuring:
- **1000+ questions** across multiple exams (JEE, NEET, UPSC, etc.)
- **Smart filtering** by exam, subject, topic, and difficulty
- **Personalized recommendations** using ML-based collaborative filtering
- **Progress tracking** with detailed analytics
- **Admin panel** to manage questions
- **User authentication** with JWT tokens

### Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **ML/AI**: Scikit-learn for recommendations
- **Deployment**: Docker, Docker Compose, Nginx

---

## Project Structure

```
question-bank/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── config.js
│   │   ├── api.js
│   │   ├── app.js
│   │   ├── auth.js
│   │   ├── dashboard.js
│   │   ├── browse.js
│   │   └── admin.js
│   ├── public/
│   └── images/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── utils.py
│   ├── ml_model.py
│   ├── schema.sql
│   ├── import_questions.py
│   ├── requirements.txt
│   ├── .env.example
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       ├── questions.py
│       ├── users.py
│       ├── recommendations.py
│       └── admin.py
├── docker-compose.yml
├── nginx.conf
└── README_SETUP.md
```

---

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Docker & Docker Compose (for containerized deployment)
- Node.js (optional, for frontend tooling)

---

## Local Development Setup

### 1. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create `.env` file from `.env.example`:

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=question_bank
DB_USER=postgres
DB_PASSWORD=your_password
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:8000,http://localhost:3000
PORT=8000
ENVIRONMENT=development
ADMIN_PASSWORD=admin123
```

#### Initialize Database

```bash
# Create database
createdb question_bank -U postgres

# Apply schema
psql -U postgres -d question_bank -f backend/schema.sql

# Import sample data
cd backend
python import_questions.py
```

#### Start Backend Server

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend Setup

#### Start Frontend Server

Since the frontend is vanilla HTML/CSS/JS, you can serve it directly:

**Using Python:**
```bash
cd frontend
python -m http.server 3000
```

**Using Node.js (http-server):**
```bash
npm install -g http-server
cd frontend
http-server -p 3000
```

**Using Docker (recommended):**
```bash
docker run -d -p 3000:80 -v $(pwd)/frontend:/usr/share/nginx/html nginx
```

The frontend will be available at `http://localhost:3000`

---

## Docker Deployment

### Using Docker Compose (Recommended)

The project includes a `docker-compose.yml` file that sets up:
- PostgreSQL database
- FastAPI backend
- Nginx frontend

#### Start All Services

```bash
docker-compose up -d
```

#### Stop All Services

```bash
docker-compose down
```

#### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f db
docker-compose logs -f frontend
```

#### Database Initialization with Docker

```bash
# Execute schema in running container
docker exec question-bank-db psql -U postgres -d question_bank -f /docker-entrypoint-initdb.d/schema.sql

# Or run import script
docker exec question-bank-backend python import_questions.py
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/verify-token` - Verify JWT token

### Questions
- `GET /api/questions` - List questions with filters
- `GET /api/questions/{id}` - Get question details
- `POST /api/questions/bookmarks` - Add question to bookmarks
- `GET /api/questions/bookmarks/user` - Get user's bookmarks
- `DELETE /api/questions/bookmarks/{id}` - Remove bookmark

### User Progress
- `POST /api/users/progress` - Record question attempt
- `GET /api/users/stats` - Get user statistics
- `GET /api/users/progress/{id}` - Get progress on specific question
- `GET /api/users/history` - Get attempt history

### Recommendations
- `GET /api/recommendations/personalized` - Get personalized recommendations
- `GET /api/recommendations/by-topic/{id}` - Get questions by topic
- `GET /api/recommendations/difficulty-progression` - Get difficulty-based progression

### Admin (requires admin_password)
- `POST /api/admin/exams` - Create exam
- `GET /api/admin/exams` - List exams
- `POST /api/admin/subjects` - Create subject
- `GET /api/admin/subjects` - List subjects
- `POST /api/admin/topics` - Create topic
- `GET /api/admin/topics` - List topics
- `POST /api/admin/questions` - Create question
- `PUT /api/admin/questions/{id}` - Update question
- `DELETE /api/admin/questions/{id}` - Delete question
- `GET /api/admin/statistics` - Get platform statistics

---

## Frontend Features

### Pages
1. **Home** - Landing page with features overview
2. **Login** - User authentication
3. **Register** - New user registration
4. **Dashboard** - User statistics, weak topics, personalized recommendations
5. **Browse** - Search and filter questions
6. **Question Detail** - View question, options, submit answer
7. **Admin** - Add/manage questions (requires password)
8. **Profile** - User profile information

### Key JavaScript Functions
- `navigateTo(page)` - Navigate between pages
- `API.login(credentials)` - Login user
- `API.getRecommendations()` - Get personalized recommendations
- `API.getQuestions(filters)` - Search/filter questions
- `API.recordProgress(questionId, isCorrect)` - Record user answer
- `showToast(message, type)` - Show notification

---

## Database Schema

### Core Tables
- **users** - User accounts and profile info
- **exams** - Exam types (JEE, NEET, UPSC, etc.)
- **subjects** - Subject areas (Math, English, etc.)
- **topics** - Topics within subjects
- **questions** - Question content
- **options** - MCQ options
- **user_progress** - User attempt history
- **bookmarks** - User's saved questions
- **user_weak_topics** - Computed weak areas

---

## ML Recommendation System

The platform uses a hybrid recommendation approach:

1. **Collaborative Filtering** - Recommends questions popular among similar users
2. **Content-Based Filtering** - Recommends questions similar to ones answered correctly
3. **User Performance Analysis** - Identifies weak topics and suggests practice questions

The ML model is trained on:
- User performance metrics (accuracy by topic)
- Question content similarity (TF-IDF)
- User target exam and experience level

---

## Troubleshooting

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U postgres -h localhost -d question_bank

# Check if service is running
systemctl status postgresql
```

### Backend Port Already in Use
```bash
# Change port in .env or kill process
lsof -i :8000
kill -9 <PID>
```

### CORS Issues
- Update `CORS_ORIGINS` in backend `.env`
- Ensure frontend and backend URLs match

### Frontend API Calls Failing
- Check API_BASE_URL in `js/config.js`
- Verify backend is running
- Check browser console for errors

---

## Importing Questions from PDFs

The platform includes a script to import questions from PDF files:

```bash
python backend/import_questions.py
```

To import custom questions:
1. Parse PDF to extract question data
2. Format as JSON with question text, options, and metadata
3. Modify `SAMPLE_QUESTIONS` in `import_questions.py`
4. Run import script

---

## Performance Optimization

### Backend
- Database indexes on frequently queried columns
- Query caching with SQLAlchemy
- Pagination for large result sets
- JWT token-based auth to reduce database queries

### Frontend
- Lazy loading of images
- Caching API responses in session storage
- Debounced search/filter functions
- Minified CSS and JavaScript

### Database
- Proper indexing on foreign keys
- Stored procedures for complex queries
- Connection pooling
- Regular vacuum and analyze

---

## Security Best Practices

1. **Authentication**
   - Passwords hashed with bcrypt
   - JWT tokens with expiration
   - HTTPS in production

2. **Authorization**
   - Role-based access control (user, admin)
   - Admin password for sensitive operations
   - RLS policies for multi-tenancy

3. **Data Protection**
   - SQL parameterization to prevent injection
   - Input validation and sanitization
   - CORS properly configured
   - Environment variables for secrets

4. **Production**
   - Change SECRET_KEY
   - Change ADMIN_PASSWORD
   - Use strong database password
   - Enable HTTPS
   - Use environment-specific configs

---

## Deployment to Production

### Vercel (Recommended for Simplicity)

1. Connect GitHub repository
2. Set environment variables in project settings
3. Deploy frontend as static site
4. Deploy backend on separate service

### AWS/GCP/Azure

1. Set up managed PostgreSQL database
2. Container Registry for Docker images
3. Kubernetes or serverless for FastAPI
4. CDN for frontend static assets
5. Load balancing and auto-scaling

### Self-Hosted (VPS)

```bash
# Update system
sudo apt update && apt upgrade

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone <repo-url>
cd question-bank

# Configure environment
cp backend/.env.example backend/.env
# Edit .env with production values

# Start services
docker-compose -f docker-compose.yml up -d

# Set up SSL with Let's Encrypt
# Configure Nginx reverse proxy
# Set up backup strategy
```

---

## Monitoring & Maintenance

### Logging
- Backend logs available via `docker-compose logs`
- Frontend errors visible in browser console
- Set up ELK stack or CloudWatch for production

### Backups
```bash
# Backup PostgreSQL
docker exec question-bank-db pg_dump -U postgres question_bank > backup.sql

# Restore from backup
docker exec -i question-bank-db psql -U postgres question_bank < backup.sql
```

### Health Checks
- Backend: `GET /health`
- API Docs: `GET /docs`
- Frontend: Check page load and API connectivity

---

## Contributing

1. Follow code style guidelines
2. Test locally before submitting
3. Document API changes
4. Update README with new features
5. Submit pull requests with clear descriptions

---

## License

This project is open source. All questions and educational content are for learning purposes.

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Review server logs for backend errors

---

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Live quiz feature
- [ ] Discussion forums
- [ ] Video explanations integration
- [ ] Offline mode
- [ ] Multiple language support
