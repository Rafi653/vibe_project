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
# Start PostgreSQL and backend services
docker-compose up -d

# View logs
docker-compose logs -f
```

This command will:
- Pull the PostgreSQL 16 Alpine image
- Build the backend application image
- Start both containers
- Create a persistent volume for PostgreSQL data
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

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health

### 5. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes all data)
docker-compose down -v
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

## Common Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Access Container Shell

```bash
# Backend container
docker-compose exec backend bash

# PostgreSQL container
docker-compose exec postgres bash
```

### Connect to PostgreSQL

```bash
# Using psql in the container
docker-compose exec postgres psql -U vibe_user -d vibe_db

# Common psql commands:
# \dt              - List all tables
# \d users         - Describe users table
# \q               - Quit
```

### Rebuild Images

```bash
# Rebuild after code changes
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# Restart with new build
docker-compose up -d --build
```

### Database Operations

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# View migration history
docker-compose exec backend alembic history

# Rollback one migration
docker-compose exec backend alembic downgrade -1

# Seed database
docker-compose exec backend python -m app.db.seed
```

### Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run with verbose output
docker-compose exec backend pytest -v

# Run specific test file
docker-compose exec backend pytest tests/test_health.py
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
docker-compose up -d
```

### 2. Make Code Changes

The backend service has a volume mount (`./backend:/app`), so changes to Python files will automatically reload the application.

### 3. View Logs

```bash
docker-compose logs -f backend
```

### 4. Run Tests

```bash
docker-compose exec backend pytest
```

### 5. Database Migrations

After modifying models:
```bash
docker-compose exec backend alembic revision --autogenerate -m "your changes"
docker-compose exec backend alembic upgrade head
```

## Production Considerations

For production deployment, consider:

1. **Use Production Dockerfile**
   - Remove volume mounts
   - Disable debug mode
   - Use production WSGI server settings

2. **Environment Variables**
   - Use strong SECRET_KEY
   - Set ENVIRONMENT=production
   - Use secure database passwords

3. **Database**
   - Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
   - Enable SSL connections
   - Regular backups

4. **Security**
   - Don't expose PostgreSQL port publicly
   - Use Docker secrets for sensitive data
   - Enable Docker security features

5. **Monitoring**
   - Add health checks
   - Configure logging
   - Set up monitoring tools

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
docker-compose ps

# Check PostgreSQL logs
docker-compose logs postgres

# Verify connection from backend
docker-compose exec backend ping postgres
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

# Rebuild from scratch
docker-compose build --no-cache
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

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Backend Database Setup Guide](backend/DATABASE_SETUP.md)
