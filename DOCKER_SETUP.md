# Docker Setup Guide

This guide explains how to run the Vibe Fitness Platform using Docker and Docker Compose.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Rafi653/vibe_project.git
cd vibe_project
```

### 2. Start All Services

```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker compose up -d

# View logs
docker compose logs -f
```

This command will:
- Pull the PostgreSQL 16 Alpine image
- Pull the Redis 7 Alpine image
- Build the backend application image
- Build the frontend application image
- Start all containers
- Create persistent volumes for PostgreSQL and Redis data
- Make the backend available at http://localhost:8000
- Make the frontend available at http://localhost:3000
- Make PostgreSQL available at localhost:5432
- Make Redis available at localhost:6379

### 3. Run Database Migrations

```bash
# Run migrations to create database tables
docker compose exec backend alembic upgrade head

# Optionally seed the database with sample data
docker compose exec backend python -m app.db.seed
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 5. Stop Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (deletes all data)
docker compose down -v
```

## Service Details

### PostgreSQL Service

- **Container Name**: `vibe_postgres`
- **Image**: `postgres:16-alpine`
- **Port**: 5432 (mapped to host)
- **Database**: `vibe_db`
- **User**: `vibe_user`
- **Password**: `vibe_password`
- **Volume**: `postgres_data` (persistent storage)

### Backend Service

- **Container Name**: `vibe_backend`
- **Build Context**: `./backend`
- **Port**: 8000 (mapped to host)
- **Dependencies**: PostgreSQL, Redis (waits for health checks)
- **Auto-reload**: Enabled in development mode
- **Health Check**: HTTP check on `/api/v1/health`

### Frontend Service

- **Container Name**: `vibe_frontend`
- **Build Context**: `./frontend`
- **Port**: 3000 (mapped to host)
- **Dependencies**: Backend
- **Auto-reload**: Enabled in development mode
- **Health Check**: HTTP check on root endpoint

### Redis Service

- **Container Name**: `vibe_redis`
- **Image**: `redis:7-alpine`
- **Port**: 6379 (mapped to host)
- **Volume**: `redis_data` (persistent storage)
- **Health Check**: Redis PING command

## Common Operations

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose logs -f redis
```

### Access Container Shell

```bash
# Backend container
docker compose exec backend bash

# Frontend container
docker compose exec frontend sh

# PostgreSQL container
docker compose exec postgres bash

# Redis container
docker compose exec redis sh
```

### Connect to Databases

**PostgreSQL:**
```bash
# Using psql in the container
docker compose exec postgres psql -U vibe_user -d vibe_db

# Common psql commands:
# \dt              - List all tables
# \d users         - Describe users table
# \q               - Quit
```

**Redis:**
```bash
# Using redis-cli in the container
docker compose exec redis redis-cli

# Common redis-cli commands:
# PING             - Test connection
# KEYS *           - List all keys (use cautiously in production)
# GET key          - Get value of key
# SET key value    - Set value of key
# exit             - Quit
```

### Rebuild Images

```bash
# Rebuild all services after code changes
docker compose build

# Rebuild specific service
docker compose build backend
docker compose build frontend

# Rebuild without cache
docker compose build --no-cache

# Restart with new build
docker compose up -d --build
```

### Database Operations

```bash
# Run migrations
docker compose exec backend alembic upgrade head

# Create a new migration
docker compose exec backend alembic revision --autogenerate -m "description"

# View migration history
docker compose exec backend alembic history

# Rollback one migration
docker compose exec backend alembic downgrade -1

# Seed database
docker compose exec backend python -m app.db.seed
```

### Running Tests

**Backend Tests:**
```bash
# Run all backend tests
docker compose exec backend pytest

# Run with verbose output
docker compose exec backend pytest -v

# Run specific test file
docker compose exec backend pytest tests/test_health.py

# Run with coverage
docker compose exec backend pytest --cov=app
```

**Frontend Tests:**
```bash
# Run frontend tests
docker compose exec frontend npm test

# Run tests in CI mode (no watch)
docker compose exec frontend npm test -- --watchAll=false

# Run tests with coverage
docker compose exec frontend npm test -- --coverage --watchAll=false
```

## Environment Variables

Environment variables can be set in a `.env` file in the project root:

**Development `.env` (optional):**
```env
# Backend Configuration
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=true

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
```

**Production `.env` (required):**
```env
# Database Configuration
POSTGRES_USER=vibe_user
POSTGRES_PASSWORD=your-strong-password-here
POSTGRES_DB=vibe_db

# Backend Configuration
SECRET_KEY=your-very-strong-secret-key-here
ENVIRONMENT=production
DEBUG=false

# Frontend Configuration
REACT_APP_API_URL=https://your-api-domain.com
```

The docker-compose files will automatically pick up these variables.

**Note:** Never commit `.env` files to version control. Use `.env.example` for templates.

## Development Workflow

### 1. Start Services

```bash
docker compose up -d
```

### 2. Make Code Changes

**Backend Changes:**
- The backend service has a volume mount (`./backend:/app`)
- Changes to Python files automatically reload the application
- No rebuild required for code changes

**Frontend Changes:**
- The frontend service has a volume mount (`./frontend:/app`)
- Changes to React files automatically reload the browser
- Hot Module Replacement (HMR) is enabled

### 3. View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### 4. Run Tests

```bash
# Backend tests
docker compose exec backend pytest

# Frontend tests
docker compose exec frontend npm test
```

### 5. Database Migrations

After modifying models:
```bash
docker compose exec backend alembic revision --autogenerate -m "your changes"
docker compose exec backend alembic upgrade head
```

### 6. Install New Dependencies

**Backend:**
```bash
# Add to requirements.txt first, then rebuild
docker compose build backend
docker compose up -d backend
```

**Frontend:**
```bash
# Option 1: Rebuild container
docker compose build frontend
docker compose up -d frontend

# Option 2: Install inside running container
docker compose exec frontend npm install <package-name>
```

## Development vs Production Setup

### Development Setup (Default)

The default `docker-compose.yml` is configured for development:

```bash
# Start development environment
docker compose up -d
```

**Development Features:**
- Hot-reload enabled for backend (Python files)
- Hot-reload enabled for frontend (React files)
- Volume mounts for live code updates
- Debug mode enabled
- All ports exposed to host
- Source code accessible in containers

### Production Setup

For production deployment, use the production compose file:

```bash
# Create .env file with production secrets
cat > .env << EOF
POSTGRES_USER=vibe_user
POSTGRES_PASSWORD=your-strong-password-here
POSTGRES_DB=vibe_db
SECRET_KEY=your-very-strong-secret-key-here
EOF

# Start production environment
docker compose -f docker-compose.prod.yml up -d
```

**Production Features:**
- Multi-stage builds for optimized images
- No volume mounts (code baked into images)
- Debug mode disabled
- Production-grade nginx for frontend
- Automatic container restart
- Non-root users for security
- Health checks enabled
- Redis for caching/sessions

**Production Checklist:**
1. **Environment Variables**
   - Use strong, randomly generated SECRET_KEY
   - Use secure database passwords
   - Set ENVIRONMENT=production
   - Configure all required environment variables

2. **Database**
   - Consider using managed PostgreSQL (AWS RDS, Google Cloud SQL)
   - Enable SSL connections
   - Configure regular backups
   - Don't expose PostgreSQL port (5432) publicly

3. **Security**
   - Don't expose Redis port (6379) publicly
   - Use Docker secrets for sensitive data
   - Enable Docker security scanning
   - Keep images updated
   - Use HTTPS/TLS for all external traffic

4. **Networking**
   - Use reverse proxy (nginx, Traefik, etc.)
   - Configure SSL/TLS certificates
   - Set up proper CORS policies
   - Use internal Docker networks

5. **Monitoring & Logging**
   - Configure centralized logging
   - Set up monitoring and alerting
   - Use health checks
   - Monitor resource usage

6. **Scaling**
   - Use Docker Swarm or Kubernetes for orchestration
   - Configure load balancing
   - Set resource limits
   - Plan for horizontal scaling

## Troubleshooting

### Port Already in Use

**Problem**: Port 3000, 8000, 5432, or 6379 is already in use

**Solution**:
```bash
# Check what's using the ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Stop the conflicting service or change the port in docker-compose.yml
```

### Container Won't Start

**Problem**: Container fails to start

**Solution**:
```bash
# Check logs for error messages
docker compose logs backend
docker compose logs frontend
docker compose logs postgres
docker compose logs redis

# Check container status
docker compose ps

# Remove containers and volumes, then recreate
docker compose down -v
docker compose up -d
```

### Database Connection Issues

**Problem**: Backend can't connect to PostgreSQL or Redis

**Solution**:
```bash
# Check if services are healthy
docker compose ps

# Check PostgreSQL logs
docker compose logs postgres

# Check Redis logs
docker compose logs redis

# Verify connection from backend
docker compose exec backend ping postgres
docker compose exec backend ping redis

# Test PostgreSQL connection
docker compose exec postgres psql -U vibe_user -d vibe_db -c "SELECT 1"

# Test Redis connection
docker compose exec redis redis-cli ping
```

### Frontend Can't Reach Backend

**Problem**: Frontend shows API connection errors

**Solution**:
```bash
# Check if backend is running and healthy
docker compose ps backend
docker compose logs backend

# Test backend health endpoint
curl http://localhost:8000/api/v1/health

# Check environment variables
docker compose exec frontend printenv | grep REACT_APP

# Verify network connectivity
docker compose exec frontend wget -O- http://backend:8000/api/v1/health
```

### Permission Issues

**Problem**: Permission denied errors

**Solution**:
```bash
# On Linux, you may need to adjust file permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker-compose up -d
```

### Image Build Failures

**Problem**: Docker build fails

**Solution**:
```bash
# Clean up Docker cache
docker system prune -a

# Rebuild specific service from scratch
docker compose build --no-cache backend
docker compose build --no-cache frontend

# Rebuild all services
docker compose build --no-cache
```

### Hot Reload Not Working

**Problem**: Code changes don't trigger reload

**Solution**:

**Backend:**
```bash
# Check if volume is mounted correctly
docker compose exec backend ls -la /app

# Restart backend service
docker compose restart backend

# Check logs for reload messages
docker compose logs -f backend
```

**Frontend:**
```bash
# Check if volume is mounted correctly
docker compose exec frontend ls -la /app

# Ensure polling is enabled (already set in docker-compose.yml)
# WATCHPACK_POLLING=true
# CHOKIDAR_USEPOLLING=true

# Restart frontend service
docker compose restart frontend

# Check logs
docker compose logs -f frontend
```

## Useful Docker Commands

```bash
# List all containers
docker ps -a

# List all images
docker images

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# View disk usage
docker system df

# Complete cleanup (use with caution!)
docker system prune -a --volumes
```

## Additional Resources

- **[DOCKER_COMMANDS.md](DOCKER_COMMANDS.md)** - Comprehensive Docker commands reference
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide for getting up and running
- **[backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)** - Database setup and operations
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)
- [nginx Docker Image](https://hub.docker.com/_/nginx)
