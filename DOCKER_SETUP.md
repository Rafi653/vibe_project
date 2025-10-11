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
# Start PostgreSQL, backend, and frontend services
docker compose up -d

# View logs
docker compose logs -f
```

This command will:
- Pull the PostgreSQL 16 Alpine image
- Build the backend application image
- Build the frontend application image
- Start all containers
- Create a persistent volume for PostgreSQL data
- Make the frontend available at http://localhost:3000
- Make the backend available at http://localhost:8000
- Make PostgreSQL available at localhost:5432

### 3. Run Database Migrations

```bash
# Run migrations to create database tables
docker-compose exec backend alembic upgrade head

# Optionally seed the database with sample data
docker-compose exec backend python -m app.db.seed
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health

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
- **Dependencies**: PostgreSQL (waits for health check)
- **Auto-reload**: Enabled in development mode
- **Health Check**: Checks `/api/v1/health` endpoint every 30s

### Frontend Service

- **Container Name**: `vibe_frontend`
- **Build Context**: `./frontend`
- **Port**: 3000 (mapped to host)
- **Dependencies**: Backend service
- **Auto-reload**: Enabled in development mode (hot module replacement)
- **Volume**: `./frontend:/app` (for hot-reload)

## Common Operations

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
```

### Access Container Shell

```bash
# Backend container
docker compose exec backend bash

# Frontend container
docker compose exec frontend sh

# PostgreSQL container
docker compose exec postgres bash
```

### Connect to PostgreSQL

```bash
# Using psql in the container
docker compose exec postgres psql -U vibe_user -d vibe_db

# Common psql commands:
# \dt              - List all tables
# \d users         - Describe users table
# \q               - Quit
```

### Rebuild Images

```bash
# Rebuild after code changes
docker compose build

# Rebuild without cache
docker compose build --no-cache

# Restart with new build
docker compose up -d --build

# Rebuild specific service
docker compose build backend
docker compose build frontend
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

```bash
# Backend tests
docker compose exec backend pytest

# Run with verbose output
docker compose exec backend pytest -v

# Run specific test file
docker compose exec backend pytest tests/test_health.py

# Frontend tests
docker compose exec frontend npm test
```

## Environment Variables

Environment variables can be set in a `.env` file in the project root:

```env
# Create .env file
cat > .env << EOF
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=true
EOF
```

The `docker-compose.yml` will automatically pick up these variables.

## Development Workflow

### 1. Start Services

```bash
docker compose up -d
```

### 2. Make Code Changes

Both frontend and backend have volume mounts for hot-reload:
- **Backend** (`./backend:/app`): Python files automatically reload
- **Frontend** (`./frontend:/app`): React Hot Module Replacement (HMR) enabled

### 3. View Logs

```bash
# Backend logs
docker compose logs -f backend

# Frontend logs
docker compose logs -f frontend

# All logs
docker compose logs -f
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

## Production Deployment

### Using Production Docker Compose

For production deployment, use the production compose file:

```bash
# Create .env file with production settings
cp .env.example .env
nano .env  # Edit with your production values

# Required environment variables for production:
# - SECRET_KEY (must be set to a strong random value)
# - POSTGRES_PASSWORD (must be set)
# - ALLOWED_ORIGINS (your production domain)

# Start production services
docker compose -f docker-compose.prod.yml up -d

# Run migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Production Features

The production setup includes:
- **Multi-stage builds** for smaller image sizes
- **Non-root user** for backend security
- **Nginx** for serving frontend with gzip compression
- **Health checks** for all services
- **Automatic restarts** on failure
- **Optimized caching** for static assets
- **Security headers** in nginx

### Production Checklist

1. **Environment Variables**
   - ✅ Use strong SECRET_KEY (generate with `openssl rand -hex 32`)
   - ✅ Set ENVIRONMENT=production
   - ✅ Disable DEBUG mode
   - ✅ Use secure database passwords
   - ✅ Configure ALLOWED_ORIGINS with your domain

2. **Database**
   - ✅ Use managed PostgreSQL service (AWS RDS, Google Cloud SQL) or ensure proper backups
   - ✅ Enable SSL connections
   - ✅ Regular automated backups
   - ✅ Don't expose PostgreSQL port publicly (remove port mapping)

3. **Security**
   - ✅ Use Docker secrets for sensitive data
   - ✅ Enable Docker security features
   - ✅ Keep images updated
   - ✅ Scan for vulnerabilities regularly

4. **Monitoring**
   - ✅ Health checks are configured
   - ✅ Configure centralized logging
   - ✅ Set up monitoring tools (Prometheus, Grafana)
   - ✅ Set up alerts for service failures

5. **Performance**
   - ✅ Backend runs with 4 workers (adjust based on CPU cores)
   - ✅ Frontend served by Nginx with compression
   - ✅ Static assets cached for 1 year
   - ✅ Database connection pooling configured

## Troubleshooting

### Port Already in Use

**Problem**: Port 8000 or 5432 is already in use

**Solution**:
```bash
# Check what's using the port
lsof -i :8000
lsof -i :5432

# Stop the conflicting service or change the port in docker-compose.yml
```

### Container Won't Start

**Problem**: Container fails to start

**Solution**:
```bash
# Check logs for error messages
docker-compose logs backend
docker-compose logs postgres

# Remove containers and volumes, then recreate
docker-compose down -v
docker-compose up -d
```

### Database Connection Issues

**Problem**: Backend can't connect to PostgreSQL

**Solution**:
```bash
# Check if PostgreSQL is healthy
docker compose ps

# Check PostgreSQL logs
docker compose logs postgres

# Verify connection from backend
docker compose exec backend ping postgres
```

### Frontend Can't Connect to Backend

**Problem**: Frontend shows API connection errors

**Solution**:
```bash
# Check if backend is running
docker compose ps

# Check backend logs for errors
docker compose logs backend

# Verify backend health
curl http://localhost:8000/api/v1/health

# Check if CORS is configured (should include http://localhost:3000)
docker compose exec backend env | grep ALLOWED_ORIGINS
```

### Hot-Reload Not Working

**Problem**: Changes to code don't trigger reload

**Solution**:

For backend:
```bash
# Ensure volume mount is working
docker compose exec backend ls -la /app

# Restart backend service
docker compose restart backend
```

For frontend:
```bash
# Check if polling is enabled
docker compose exec frontend env | grep CHOKIDAR

# Restart frontend service
docker compose restart frontend

# On some systems, you may need to increase file watchers
# On Linux host:
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Permission Issues

**Problem**: Permission denied errors

**Solution**:
```bash
# On Linux, you may need to adjust file permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker compose up -d
```

### Image Build Failures

**Problem**: Docker build fails

**Solution**:
```bash
# Clean up Docker cache
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache

# Build specific service
docker compose build --no-cache backend
docker compose build --no-cache frontend
```

### Frontend Build Out of Memory

**Problem**: Frontend build fails with "JavaScript heap out of memory"

**Solution**:
```bash
# Increase Node.js memory limit in docker-compose.yml
# Add to frontend service environment:
# - NODE_OPTIONS=--max_old_space_size=4096
```

## Docker Image Optimization

### Image Sizes

Our Docker images are optimized for production:

**Development:**
- Backend: ~500MB (includes dev tools and volume mount)
- Frontend: ~300MB (Node.js with dev server)

**Production:**
- Backend: ~200MB (multi-stage build, non-root user)
- Frontend: ~25MB (multi-stage build with nginx Alpine)
- PostgreSQL: ~240MB (official Alpine image)

### Optimization Features

**Backend:**
- ✅ Multi-stage build separates build and runtime dependencies
- ✅ Python 3.11-slim base image
- ✅ Minimal system dependencies
- ✅ Non-root user for security
- ✅ Layer caching for requirements.txt

**Frontend:**
- ✅ Multi-stage build (build stage + nginx stage)
- ✅ Node.js Alpine for smaller size
- ✅ Production build optimization
- ✅ Static assets served by nginx
- ✅ Gzip compression enabled
- ✅ Long-term caching for static assets

### Further Optimization Tips

1. **Use .dockerignore**: Exclude unnecessary files from build context
2. **Order layers**: Put frequently changing files last
3. **Combine RUN commands**: Reduce layer count
4. **Use specific versions**: Pin base image versions for reproducibility
5. **Clean up in same layer**: Remove temporary files in the same RUN command

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

# Check image size
docker images vibe_project*

# Inspect image layers
docker history <image-name>
```

## Quick Command Reference

For a quick reference of common Docker commands, see [DOCKER_QUICK_REFERENCE.md](DOCKER_QUICK_REFERENCE.md).

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Backend Database Setup Guide](backend/DATABASE_SETUP.md)
- [Docker Quick Reference](DOCKER_QUICK_REFERENCE.md)
