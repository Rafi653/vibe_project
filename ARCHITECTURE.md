# Vibe Fitness Platform - Architecture Documentation

This document provides a comprehensive overview of the Vibe Fitness Platform's system architecture, design patterns, and technical decisions.

## Table of Contents
- [System Overview](#system-overview)
- [Architecture Diagrams](#architecture-diagrams)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Database Design](#database-design)
- [Authentication & Authorization](#authentication--authorization)
- [API Design](#api-design)
- [Data Flow](#data-flow)
- [Security](#security)
- [Performance](#performance)
- [Scalability](#scalability)

## System Overview

The Vibe Fitness Platform is a full-stack web application for fitness coaching and tracking, built with modern technologies and best practices.

### Technology Stack

**Backend:**
- **Framework**: FastAPI 0.115.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL 16+
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: JWT with python-jose
- **Migration**: Alembic
- **Testing**: pytest + pytest-asyncio

**Frontend:**
- **Framework**: React 19.2.0
- **Routing**: React Router DOM 7.9.4
- **Build Tool**: Create React App
- **Charts**: Chart.js + react-chartjs-2
- **Testing**: Jest + React Testing Library

**Infrastructure:**
- **Server**: Uvicorn (ASGI)
- **Reverse Proxy**: Nginx (production)
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

### Design Principles

1. **Separation of Concerns**: Clear boundaries between layers
2. **Modularity**: Loosely coupled components
3. **Testability**: Easy to test in isolation
4. **Security First**: Authentication and authorization at every level
5. **Async by Default**: Non-blocking I/O for better performance
6. **API-First**: Well-designed REST API
7. **Type Safety**: Type hints in Python, PropTypes in React

## Architecture Diagrams

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                         │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │   Browser  │  │   Mobile   │  │   Desktop App       │   │
│  │            │  │  (Future)  │  │   (Future)          │   │
│  └─────┬──────┘  └──────┬─────┘  └──────────┬──────────┘   │
└────────┼────────────────┼───────────────────┼───────────────┘
         │                │                   │
         └────────────────┴───────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              React Frontend (Port 3000)              │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │   │
│  │  │ Components │  │   Pages    │  │   Services   │  │   │
│  │  └────────────┘  └────────────┘  └──────────────┘  │   │
│  │  ┌────────────┐  ┌────────────┐                     │   │
│  │  │  Context   │  │   Hooks    │                     │   │
│  │  └────────────┘  └────────────┘                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS/REST API
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       API GATEWAY LAYER                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          FastAPI Application (Port 8000)             │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │        CORS Middleware                        │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │  API       │  │  Services  │  │   Dependencies      │   │
│  │  Routes    │  │  (Business │  │   (Auth, DI)        │   │
│  │            │  │   Logic)   │  │                     │   │
│  └────────────┘  └────────────┘  └─────────────────────┘   │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐   │
│  │  Schemas   │  │   Core     │  │    Security         │   │
│  │ (Pydantic) │  │  (Config)  │  │  (JWT, Password)    │   │
│  └────────────┘  └────────────┘  └─────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SQLAlchemy 2.0 (Async)                  │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │   │
│  │  │   Models   │  │    Base    │  │   Sessions   │  │   │
│  │  └────────────┘  └────────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           PostgreSQL 16+ (Port 5432)                 │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐   │   │
│  │  │ Users  │ │Workout │ │  Diet  │ │   Plans    │   │   │
│  │  │        │ │  Logs  │ │  Logs  │ │            │   │   │
│  │  └────────┘ └────────┘ └────────┘ └────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

```
User Request Flow:
==================

1. User Action (Browser)
   ↓
2. React Component Handler
   ↓
3. Service Layer (API Call)
   ↓
4. HTTP Request → Backend API
   ↓
5. FastAPI Route Handler
   ↓
6. Authentication Middleware
   ↓
7. Authorization Check (Role-based)
   ↓
8. Business Logic (Service Layer)
   ↓
9. Database Query (SQLAlchemy)
   ↓
10. PostgreSQL Database
    ↓
11. Response Data
    ↓
12. Pydantic Schema Validation
    ↓
13. JSON Response
    ↓
14. Frontend Service Parser
    ↓
15. React State Update
    ↓
16. UI Re-render
```

## Backend Architecture

### Layered Architecture

The backend follows a clean, layered architecture pattern:

```
┌─────────────────────────────────────┐
│         API Layer (Routes)          │  ← HTTP endpoints
├─────────────────────────────────────┤
│       Service Layer (Logic)         │  ← Business logic
├─────────────────────────────────────┤
│    Data Access Layer (Models)       │  ← Database operations
├─────────────────────────────────────┤
│         Database (PostgreSQL)       │  ← Data storage
└─────────────────────────────────────┘
```

### Directory Structure

```
backend/app/
├── api/                    # API layer
│   └── v1/                # Version 1 endpoints
│       ├── auth.py        # Authentication endpoints
│       ├── client.py      # Client endpoints
│       ├── coach.py       # Coach endpoints
│       ├── admin.py       # Admin endpoints
│       └── users.py       # User management
├── core/                   # Core utilities
│   ├── config.py          # Configuration
│   ├── security.py        # JWT, password hashing
│   └── dependencies.py    # Dependency injection
├── models/                 # Database models
│   ├── user.py
│   ├── workout_log.py
│   ├── diet_log.py
│   ├── workout_plan.py
│   └── diet_plan.py
├── schemas/                # Pydantic schemas
│   ├── auth.py
│   ├── user.py
│   └── ...
├── services/               # Business logic
│   └── auth_service.py
├── db/                     # Database utilities
│   ├── base.py
│   └── seed.py
└── main.py                 # Application entry point
```

### Key Design Patterns

**1. Dependency Injection**
```python
# Using FastAPI's dependency injection
@router.get("/me")
async def get_current_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    return current_user
```

**2. Repository Pattern**
```python
# Models act as repositories with SQLAlchemy
result = await db.execute(
    select(User).where(User.email == email)
)
user = result.scalar_one_or_none()
```

**3. Service Layer Pattern**
```python
# Business logic in service classes
class AuthService:
    @staticmethod
    async def signup_user(db: AsyncSession, user_data: UserSignup):
        # Validate, hash password, create user, generate token
        ...
```

**4. Schema Validation**
```python
# Pydantic models for request/response validation
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
```

### Async Architecture

All I/O operations are asynchronous:

```python
# Async database sessions
async with AsyncSessionLocal() as session:
    result = await session.execute(query)
    
# Async endpoint handlers
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

## Frontend Architecture

### Component Hierarchy

```
App (Router)
├── Navigation
├── ProtectedRoute
│   ├── ClientDashboard
│   │   ├── LineChart
│   │   ├── BarChart
│   │   └── DoughnutChart
│   ├── CoachDashboard
│   │   ├── LineChart
│   │   ├── BarChart
│   │   └── DoughnutChart
│   └── AdminDashboard
│       ├── LineChart
│       ├── BarChart
│       └── DoughnutChart
├── Login
├── Signup
└── Home
```

### State Management

**AuthContext**: Manages authentication state globally

```javascript
<AuthProvider>
  <App />
</AuthProvider>
```

**Local State**: Component-specific state with useState

```javascript
const [workouts, setWorkouts] = useState([]);
const [loading, setLoading] = useState(false);
```

### Service Layer

API calls are abstracted in service modules:

```javascript
// services/authService.js
export const login = async (credentials) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    body: JSON.stringify(credentials)
  });
  return response.json();
};
```

## Database Design

### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐
│    Users     │       │ WorkoutLogs  │
├──────────────┤       ├──────────────┤
│ id (PK)      │───┐   │ id (PK)      │
│ email        │   │   │ user_id (FK) │
│ password     │   └──<│ workout_date │
│ full_name    │       │ exercise     │
│ role         │       │ sets/reps    │
│ is_active    │       └──────────────┘
│ created_at   │
└──────────────┘       ┌──────────────┐
       │               │  DietLogs    │
       │               ├──────────────┤
       └──────────────<│ id (PK)      │
       │               │ user_id (FK) │
       │               │ meal_date    │
       │               │ meal_type    │
       │               │ calories     │
       │               └──────────────┘
       │
       │               ┌──────────────┐
       │               │WorkoutPlans  │
       │               ├──────────────┤
       └──────────────<│ id (PK)      │
       │               │ user_id (FK) │
       │               │ plan_name    │
       │               │ start_date   │
       │               │ status       │
       │               └──────────────┘
       │
       │               ┌──────────────┐
       │               │  DietPlans   │
       │               ├──────────────┤
       └──────────────<│ id (PK)      │
                       │ user_id (FK) │
                       │ plan_name    │
                       │ target_cals  │
                       │ status       │
                       └──────────────┘
```

### Key Tables

**users**: User accounts and authentication
- Primary key: `id`
- Unique: `email`
- Indexed: `role`, `is_active`

**workout_logs**: Daily workout tracking
- Primary key: `id`
- Foreign key: `user_id` → users(id)
- Indexed: `user_id`, `workout_date`

**diet_logs**: Meal tracking
- Primary key: `id`
- Foreign key: `user_id` → users(id)
- Indexed: `user_id`, `meal_date`

**workout_plans**: Structured workout programs
- Primary key: `id`
- Foreign key: `user_id` → users(id)
- Indexed: `user_id`, `status`

**diet_plans**: Nutrition plans
- Primary key: `id`
- Foreign key: `user_id` → users(id)
- Indexed: `user_id`, `status`

See [DATABASE_SCHEMA.md](backend/DATABASE_SCHEMA.md) for detailed schema information.

## Authentication & Authorization

### Authentication Flow

```
1. User submits credentials
   ↓
2. Backend verifies password
   ↓
3. Generate JWT token with user info
   ↓
4. Return token to client
   ↓
5. Client stores token (localStorage)
   ↓
6. Client includes token in all requests
   ↓
7. Backend validates token
   ↓
8. Extract user from token
   ↓
9. Check user permissions
   ↓
10. Process request
```

### JWT Token Structure

```json
{
  "sub": "user@example.com",
  "user_id": 123,
  "role": "client",
  "exp": 1234567890
}
```

### Role-Based Access Control

```python
# Three roles with hierarchy
UserRole.CLIENT    # Can access client endpoints
UserRole.COACH     # Can access coach + client endpoints
UserRole.ADMIN     # Can access all endpoints
```

See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed authentication documentation.

## API Design

### REST Principles

- **Resources as nouns**: `/users`, `/workouts`
- **HTTP methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Stateless**: Each request contains all necessary information
- **Versioned**: `/api/v1/...`

### Endpoint Structure

```
/api/v1/
├── auth/              # Authentication
│   ├── signup         # POST - Register
│   ├── login          # POST - Login
│   ├── logout         # POST - Logout
│   └── me             # GET - Current user
├── client/            # Client operations
│   ├── workout-logs   # GET, POST
│   ├── diet-logs      # GET, POST
│   └── progress       # GET
├── coach/             # Coach operations
│   ├── clients        # GET
│   └── workout-plans  # GET, POST
└── admin/             # Admin operations
    ├── users          # GET, PUT, DELETE
    └── stats          # GET
```

See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation.

## Data Flow

### Creating a Workout Log

```
1. User fills form in ClientDashboard
   ↓
2. Form submits to handleCreateWorkout()
   ↓
3. clientService.createWorkoutLog() called
   ↓
4. POST /api/v1/client/workout-logs
   ↓
5. FastAPI receives request
   ↓
6. Auth middleware validates token
   ↓
7. Route handler in client.py
   ↓
8. Pydantic validates request body
   ↓
9. Create WorkoutLog model
   ↓
10. Save to database
    ↓
11. Return WorkoutLogResponse
    ↓
12. Frontend updates state
    ↓
13. UI refreshes to show new log
```

## Security

### Security Measures

1. **Password Hashing**: bcrypt with salt
2. **JWT Tokens**: Signed with secret key
3. **HTTPS Only**: Force SSL in production
4. **CORS**: Configured allowed origins
5. **SQL Injection**: Prevented by ORM
6. **XSS**: React escapes by default
7. **CSRF**: Stateless JWT (no cookies)
8. **Rate Limiting**: (Future) API throttling

### Environment Variables

Sensitive data stored in environment variables:
- `SECRET_KEY`: JWT signing key
- `DATABASE_URL`: Database connection
- `ALLOWED_ORIGINS`: CORS configuration

## Performance

### Optimization Strategies

**Backend:**
- Async I/O for all database operations
- Connection pooling with SQLAlchemy
- Indexed database queries
- Efficient query design

**Frontend:**
- Code splitting with React.lazy
- Memoization with useMemo/useCallback
- Debounced API calls
- Optimized re-renders

**Database:**
- Proper indexing on foreign keys and frequently queried columns
- Query optimization with EXPLAIN ANALYZE
- Connection pooling

## Scalability

### Horizontal Scaling

```
              ┌──────────────┐
              │ Load Balancer│
              └──────┬───────┘
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │  API    │  │  API    │  │  API    │
   │Instance │  │Instance │  │Instance │
   └────┬────┘  └────┬────┘  └────┬────┘
        └────────────┼────────────┘
                     │
              ┌──────▼───────┐
              │  PostgreSQL  │
              │  (Primary)   │
              └──────┬───────┘
                     │
          ┌──────────┴──────────┐
          │                     │
    ┌─────▼─────┐        ┌─────▼─────┐
    │PostgreSQL │        │PostgreSQL │
    │ (Replica) │        │ (Replica) │
    └───────────┘        └───────────┘
```

### Future Enhancements

- Caching layer (Redis)
- Message queue (RabbitMQ/Celery)
- CDN for static assets
- Read replicas for database
- Microservices architecture

## Deployment Architecture

### Development

```
Docker Compose:
├── Backend (uvicorn --reload)
├── Frontend (npm start)
└── PostgreSQL
```

### Production

```
├── Nginx (Reverse proxy, SSL termination)
├── Backend (Multiple uvicorn workers)
├── Frontend (Static files served by Nginx)
└── PostgreSQL (Managed service or dedicated server)
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for deployment details.

## Monitoring & Logging

### Logging Strategy

**Backend:**
- Structured logging with Python logging module
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Logs include timestamp, level, module, and message

**Frontend:**
- Console logging in development
- Error tracking service in production (Future: Sentry)

### Metrics

Track:
- API response times
- Error rates
- Database query performance
- User authentication events
- Resource usage (CPU, memory)

## Conclusion

The Vibe Fitness Platform is built with modern, scalable architecture patterns that support:
- Clean separation of concerns
- Easy testing and maintenance
- Security by default
- Performance optimization
- Future scalability

For more detailed information, see the specific documentation files referenced throughout this document.
