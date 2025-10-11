# Vibe Fitness Platform - Backend API

Backend API for the Vibe Fitness Coaching Platform, built with Python and FastAPI.

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Runtime**: Python 3.11+
- **Server**: Uvicorn with ASGI
- **Database**: PostgreSQL with SQLAlchemy 2.0 (async)
- **Authentication**: JWT with python-jose
- **Testing**: pytest with async support

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   │   └── v1/           # API version 1 endpoints
│   │       └── health.py # Health check endpoint
│   ├── core/             # Core configuration
│   │   └── config.py     # Application settings
│   ├── db/               # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── main.py           # Application entry point
├── tests/                # Test files
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- PostgreSQL 16+ (or use Docker - recommended)
- Docker Desktop (optional but recommended for easy setup)

### Installation

1. **Create a virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up the database**:
   
   **Option A: Using Docker (Recommended)**
   ```bash
   # From the project root directory
   cd ..
   docker-compose up -d postgres
   cd backend
   
   # Run migrations
   alembic upgrade head
   
   # Seed the database (optional)
   python -m app.db.seed
   ```
   
   **Option B: Local PostgreSQL**
   See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed instructions.

### Running the Application

**Development mode with auto-reload**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API Root: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/api/docs
- Alternative API docs (ReDoc): http://localhost:8000/api/redoc
- OpenAPI schema: http://localhost:8000/api/openapi.json

### Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health status

### Root
- `GET /` - API welcome message and version info

## Development

### Adding New Endpoints

1. Create a new router file in `app/api/v1/`
2. Define your endpoints using FastAPI route decorators
3. Include the router in `app/main.py`

Example:
```python
# app/api/v1/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"users": []}
```

```python
# app/main.py
from app.api.v1 import users

app.include_router(users.router, prefix="/api/v1", tags=["users"])
```

### Code Style

This project follows Python best practices:
- PEP 8 style guide
- Type hints for better code clarity
- Async/await for asynchronous operations

## Environment Variables

Key environment variables (see `.env.example` for all options):

- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `ENVIRONMENT`: Environment (development/staging/production)
- `DEBUG`: Enable debug mode
- `HOST`: Server host
- `PORT`: Server port
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `ALLOWED_ORIGINS`: CORS allowed origins

## Database

The application uses PostgreSQL with SQLAlchemy 2.0 (async) and Alembic for migrations.

### Data Models
- **User**: User accounts with roles (client, coach, admin)
- **WorkoutLog**: Individual workout session tracking
- **DietLog**: Daily meal and nutrition tracking
- **WorkoutPlan**: Structured workout programs
- **DietPlan**: Structured diet programs

### Quick Start
```bash
# Using Docker (easiest)
docker-compose up -d
docker-compose exec backend alembic upgrade head

# See DATABASE_SETUP.md for detailed setup instructions
```

For comprehensive database documentation, see [DATABASE_SETUP.md](DATABASE_SETUP.md).

## Next Steps

- Implement authentication and authorization
- Create user management endpoints
- Add workout and coaching features
- Set up background tasks for notifications
- Configure production deployment

## Contributing

Please follow the existing code structure and style. Ensure all tests pass before submitting changes.

## License

TBD
