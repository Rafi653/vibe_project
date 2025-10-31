# Vibe Project - Fitness Coaching App

## Project Overview
Vibe Project is a comprehensive fitness coaching application designed to connect fitness enthusiasts with professional coaches, provide personalized workout plans, track progress, and foster a supportive fitness community. The platform aims to make professional fitness coaching accessible and engaging through modern technology.

## High-Level Goals
- **Personalized Coaching**: Enable users to connect with certified fitness coaches and receive tailored workout plans
- **Progress Tracking**: Provide comprehensive tools for tracking workouts, nutrition, and fitness metrics
- **Community Engagement**: Build a supportive community where users can share their fitness journey
- **Accessibility**: Make professional fitness coaching accessible to users of all fitness levels
- **Data-Driven Insights**: Leverage analytics to help users and coaches make informed decisions ✅

## Key Features

### 💬 In-App Chat (NEW!)
Real-time messaging system for seamless communication:
- **Direct Messaging**: 1:1 conversations between users
- **Group Chats**: Create and manage group conversations
- **Real-time Updates**: WebSocket-based instant messaging
- **Typing Indicators**: See when others are typing
- **Read Receipts**: Know when messages are read
- **Active User Tracking**: See who's online
- **Message Management**: Edit and delete your messages

See [CHAT_FEATURE.md](CHAT_FEATURE.md) and [CHAT_QUICK_START.md](CHAT_QUICK_START.md) for details.

### 📊 Charts and Dashboards
Interactive charts and analytics for tracking progress and engagement:
- **Client Dashboard**: Workout frequency, diet adherence, macros tracking, strength progress
- **Coach Dashboard**: Client activity overview, engagement trends, plan assignments
- **Admin Dashboard**: User growth, platform usage, system health indicators

See [CHARTS_QUICK_START.md](CHARTS_QUICK_START.md) and [CHARTS_DOCUMENTATION.md](CHARTS_DOCUMENTATION.md) for details.

## Architecture & Tech Stack

### Frontend
- **Framework**: React.js 19.2.0 ✅
- **Routing**: React Router DOM 7.9.4 ✅
- **Charts**: Chart.js 4.x with react-chartjs-2 ✅
- **Styling**: CSS (TailwindCSS or Material-UI for future enhancement)
- **State Management**: Context API ✅
- **Mobile**: React Native (future consideration)

### Backend
- **Framework**: FastAPI 0.115.0 ✅
- **Runtime**: Python 3.11+ ✅
- **Database**: PostgreSQL 16+ with SQLAlchemy 2.0 (async) ✅
- **Authentication**: JWT-based authentication ✅
- **API**: RESTful API ✅
- **Testing**: pytest with 70% code coverage ✅
- **CI/CD**: GitHub Actions ✅

### Additional Services
- **File Storage**: AWS S3 or similar for media files
- **Real-time Features**: WebSockets for live chat updates ✅
- **Email Service**: SendGrid or AWS SES
- **Analytics**: Google Analytics, Mixpanel

## Directory Structure
```
vibe_project/
├── backend/          # Backend API and server-side logic
├── frontend/         # Frontend application and UI components
├── README.md         # Project documentation (this file)
└── .gitignore        # Git ignore rules
```

## Getting Started

### Quick Start with Docker (Recommended) 🐳

The easiest way to get started is using Docker. All services (PostgreSQL, Backend, Frontend) are containerized:

```bash
# Start all services (PostgreSQL + Backend + Frontend)
docker compose up -d

# View logs
docker compose logs -f

# Run database migrations
docker compose exec backend alembic upgrade head

# Seed the database with test data (optional)
docker compose exec backend python -m app.db.seed

# Seed with comprehensive chart data (recommended for charts feature)
docker compose exec backend python -m app.db.seed_charts
```

Access the application:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health

Stop services:
```bash
docker compose down
```

For detailed Docker setup instructions, troubleshooting, and production deployment, see:
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Complete guide
- [DOCKER_QUICK_REFERENCE.md](DOCKER_QUICK_REFERENCE.md) - Quick command reference

### 🌐 Share Your App with ngrok

Want to share your local app with friends or testers? Use ngrok to expose your app to the internet!

```bash
# Quick start
./scripts/start-ngrok.sh
```

See [NGROK_SETUP.md](NGROK_SETUP.md) for complete setup instructions, security considerations, and troubleshooting.

### Frontend Setup
The frontend is built with React.js and includes role-based navigation for clients, coaches, and administrators.

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

For more details, see the [Frontend README](frontend/README.md).

### Backend Setup (Without Docker)
The backend is built with Python and FastAPI. To get started:

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Follow the setup instructions in [backend/README.md](backend/README.md)

Quick start:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database (see backend/DATABASE_SETUP.md)
alembic upgrade head

# Run the application
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with interactive docs at http://localhost:8000/api/docs

## Testing

The project has comprehensive test coverage to ensure code quality and reliability.

### Running Tests

**Backend:**
```bash
cd backend
pytest --cov=app tests/
```

**Frontend:**
```bash
cd frontend
npm test
```

**Current Coverage:**
- Backend: **70%** ✅ (Target: 70%+)
- Frontend: Tests available

See [TESTING.md](TESTING.md) for detailed testing documentation.

### CI/CD

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

The GitHub Actions workflow includes:
- Backend tests with coverage reporting
- Frontend tests with coverage reporting
- Code linting checks

## Documentation

Comprehensive documentation is available for developers:

- **[QUICK_START.md](QUICK_START.md)** - Quick start guide for new users
- **[TESTING.md](TESTING.md)** - Testing guide and best practices
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Authentication system details
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Docker deployment guide
- **[CHARTS_DOCUMENTATION.md](CHARTS_DOCUMENTATION.md)** - Charts and dashboards guide
- **[NGROK_SETUP.md](NGROK_SETUP.md)** - Share your app publicly with ngrok
- **[NGROK_QUICK_REFERENCE.md](NGROK_QUICK_REFERENCE.md)** - Quick ngrok commands

### API Documentation

Interactive API documentation is available when running the backend:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) guide to get started.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'feat: add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Coding Standards

- **Backend**: Follow PEP 8, use type hints, write async code
- **Frontend**: Follow ESLint config, use functional components
- **Tests**: Maintain 70%+ coverage for backend
- **Documentation**: Update docs with your changes

## Team Onboarding

Welcome to the Vibe Project! This repository is structured to separate frontend and backend concerns clearly:
- `/backend` - All server-side code, APIs, database models, and business logic
- `/frontend` - All client-side code, UI components, and user-facing features

**New Developer Checklist:**
1. Read [QUICK_START.md](QUICK_START.md) for setup instructions
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
3. Read [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
4. Set up your development environment (Docker recommended)
5. Run tests to verify your setup
6. Pick an issue labeled "good first issue" to get started

## License
TBD

## Contact
For questions or contributions, please refer to the project issues and discussions.