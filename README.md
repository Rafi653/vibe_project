# Vibe Project - Fitness Coaching App

## Project Overview
Vibe Project is a comprehensive fitness coaching application designed to connect fitness enthusiasts with professional coaches, provide personalized workout plans, track progress, and foster a supportive fitness community. The platform aims to make professional fitness coaching accessible and engaging through modern technology.

## High-Level Goals
- **Personalized Coaching**: Enable users to connect with certified fitness coaches and receive tailored workout plans
- **Progress Tracking**: Provide comprehensive tools for tracking workouts, nutrition, and fitness metrics
- **Community Engagement**: Build a supportive community where users can share their fitness journey
- **Accessibility**: Make professional fitness coaching accessible to users of all fitness levels
- **Data-Driven Insights**: Leverage analytics to help users and coaches make informed decisions

## Architecture & Tech Stack

### Frontend
- **Framework**: React.js 19.2.0 ✅
- **Routing**: React Router DOM 7.9.4 ✅
- **Styling**: CSS (TailwindCSS or Material-UI for future enhancement)
- **State Management**: Redux or Context API (to be implemented)
- **Mobile**: React Native (future consideration)

### Backend
- **Runtime**: Node.js with Express.js or Python with FastAPI/Django
- **Database**: PostgreSQL for relational data, Redis for caching
- **Authentication**: JWT-based authentication with OAuth support
- **API**: RESTful API with potential GraphQL integration
- **Cloud Infrastructure**: AWS or Google Cloud Platform

### Additional Services
- **File Storage**: AWS S3 or similar for media files
- **Real-time Features**: WebSockets for live updates
- **Email Service**: SendGrid or AWS SES
- **Analytics**: Google Analytics, Mixpanel

## Directory Structure
```
vibe_project/
├── .github/          # GitHub-specific files (issue templates, workflows)
├── backend/          # Backend API and server-side logic
├── frontend/         # Frontend application and UI components
├── README.md         # Project documentation (this file)
└── .gitignore        # Git ignore rules
```

## Project Roadmap
This project follows a structured development roadmap outlined in [Issue #1](https://github.com/Rafi653/vibe_project/issues/1). The development is broken down into 10 sequential steps:

1. ✅ Initialize Repository Structure (Completed)
2. 🚧 Set Up Backend Framework ([Issue #4](https://github.com/Rafi653/vibe_project/issues/4))
3. 🚧 Set Up Frontend Framework ([Issue #5](https://github.com/Rafi653/vibe_project/issues/5))
4. 🚧 Database Setup ([Issue #6](https://github.com/Rafi653/vibe_project/issues/6))
5. ⬜ Authentication & Role-Based Access Control
6. ⬜ Core Features Implementation
7. ⬜ Charts and Dashboards
8. ⬜ Dockerization
9. ⬜ Testing & Documentation
10. ⬜ Deployment Preparation

For detailed issue templates and creation scripts, see the [`.github` directory](.github/README.md).

## Getting Started

### Quick Start with Docker (Recommended)

The easiest way to get started is using Docker:

```bash
# Start all services (PostgreSQL + Backend)
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed the database (optional)
docker-compose exec backend python -m app.db.seed
```

Access the application:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health

For detailed Docker setup instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

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

## Team Onboarding
Welcome to the Vibe Project! This repository is structured to separate frontend and backend concerns clearly:
- `/backend` - All server-side code, APIs, database models, and business logic
- `/frontend` - All client-side code, UI components, and user-facing features

Stay tuned for more detailed setup instructions as we scaffold the project further.

## License
TBD

## Contact
For questions or contributions, please refer to the project issues and discussions.