# Docker Commands Quick Reference

This is a quick reference guide for common Docker commands used in the Vibe Fitness Platform.

## 🚀 Getting Started

### Start All Services
```bash
# Development mode (with hot-reload)
docker compose up -d

# View startup logs
docker compose up

# Production mode
docker compose -f docker-compose.prod.yml up -d
```

### Stop Services
```bash
# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes all data)
docker compose down -v

# Stop specific service
docker compose stop backend
docker compose stop frontend
```

## 📊 Monitoring & Logs

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose logs -f redis

# Last 100 lines
docker compose logs --tail=100 backend

# Since specific time
docker compose logs --since 30m backend
```

### Check Service Status
```bash
# List running containers
docker compose ps

# Detailed container info
docker compose ps -a

# Check health status
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"
```

### View Resource Usage
```bash
# Real-time stats
docker stats

# One-time stats
docker stats --no-stream

# Specific containers
docker stats vibe_backend vibe_frontend
```

## 🔧 Building & Rebuilding

### Build Images
```bash
# Build all services
docker compose build

# Build specific service
docker compose build backend
docker compose build frontend

# Build without cache (fresh build)
docker compose build --no-cache

# Build and start
docker compose up -d --build
```

### Pull Latest Images
```bash
# Pull all base images
docker compose pull

# Pull specific service
docker compose pull postgres
docker compose pull redis
```

## 🐛 Debugging

### Access Container Shell
```bash
# Backend (bash)
docker compose exec backend bash

# Frontend (sh)
docker compose exec frontend sh

# PostgreSQL (bash)
docker compose exec postgres bash

# Redis (sh)
docker compose exec redis sh
```

### Execute Commands in Container
```bash
# Backend commands
docker compose exec backend python --version
docker compose exec backend pytest
docker compose exec backend alembic current

# Frontend commands
docker compose exec frontend npm --version
docker compose exec frontend npm test
docker compose exec frontend npm run build
```

### Inspect Containers
```bash
# View container details
docker inspect vibe_backend

# View container logs path
docker inspect vibe_backend | grep LogPath

# View environment variables
docker compose exec backend env
docker compose exec frontend env
```

## 💾 Database Operations

### PostgreSQL
```bash
# Connect to database
docker compose exec postgres psql -U vibe_user -d vibe_db

# Run SQL commands
docker compose exec postgres psql -U vibe_user -d vibe_db -c "SELECT COUNT(*) FROM users;"

# Backup database
docker compose exec postgres pg_dump -U vibe_user vibe_db > backup.sql

# Restore database
docker compose exec -T postgres psql -U vibe_user -d vibe_db < backup.sql

# View database size
docker compose exec postgres psql -U vibe_user -d vibe_db -c "SELECT pg_size_pretty(pg_database_size('vibe_db'));"
```

### Redis
```bash
# Connect to Redis
docker compose exec redis redis-cli

# Check Redis info
docker compose exec redis redis-cli INFO

# Flush all data (⚠️ use with caution)
docker compose exec redis redis-cli FLUSHALL

# Monitor Redis commands
docker compose exec redis redis-cli MONITOR
```

### Migrations
```bash
# Run migrations
docker compose exec backend alembic upgrade head

# Create new migration
docker compose exec backend alembic revision --autogenerate -m "description"

# View migration history
docker compose exec backend alembic history

# Rollback migration
docker compose exec backend alembic downgrade -1

# Seed database
docker compose exec backend python -m app.db.seed
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
docker compose exec backend pytest

# Run with verbose output
docker compose exec backend pytest -v

# Run specific test file
docker compose exec backend pytest tests/test_health.py

# Run with coverage
docker compose exec backend pytest --cov=app --cov-report=html

# Run specific test
docker compose exec backend pytest tests/test_health.py::test_health_check
```

### Frontend Tests
```bash
# Run tests (interactive mode)
docker compose exec frontend npm test

# Run tests (CI mode)
docker compose exec frontend npm test -- --watchAll=false

# Run with coverage
docker compose exec frontend npm test -- --coverage --watchAll=false
```

## 🧹 Cleanup

### Remove Stopped Containers
```bash
# Remove stopped containers
docker container prune

# Force remove all stopped containers
docker container prune -f
```

### Remove Unused Images
```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Force remove
docker image prune -af
```

### Remove Volumes
```bash
# Remove unused volumes (⚠️ be careful)
docker volume prune

# List volumes
docker volume ls

# Remove specific volume
docker volume rm vibe_project_postgres_data
```

### Complete Cleanup
```bash
# Remove everything (⚠️ use with extreme caution)
docker system prune -a --volumes

# Show space usage
docker system df

# Show detailed space usage
docker system df -v
```

## 🔄 Restart & Reload

### Restart Services
```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart backend
docker compose restart frontend

# Restart with rebuild
docker compose up -d --build
```

### Reload Configuration
```bash
# Reload after docker-compose.yml changes
docker compose up -d --force-recreate

# Reload specific service
docker compose up -d --force-recreate backend
```

## 📦 Working with Dependencies

### Backend Dependencies
```bash
# Install new Python package
# 1. Add to requirements.txt
# 2. Rebuild container
docker compose build backend
docker compose up -d backend

# Or install directly (not persistent)
docker compose exec backend pip install package-name
```

### Frontend Dependencies
```bash
# Install new npm package
# 1. Add to package.json or
docker compose exec frontend npm install package-name

# 2. Rebuild container for persistent installation
docker compose build frontend
docker compose up -d frontend
```

## 🌐 Networking

### View Networks
```bash
# List networks
docker network ls

# Inspect network
docker network inspect vibe_project_vibe_network

# Test connectivity between containers
docker compose exec backend ping postgres
docker compose exec backend ping redis
docker compose exec frontend ping backend
```

### Port Mapping
```bash
# View port mappings
docker compose port backend 8000
docker compose port frontend 3000

# Check if ports are in use
lsof -i :3000
lsof -i :8000
lsof -i :5432
lsof -i :6379
```

## 🔐 Security

### Scan Images for Vulnerabilities
```bash
# Scan image (if Docker Scout is available)
docker scout cves vibe_project-backend
docker scout cves vibe_project-frontend

# View image history
docker history vibe_project-backend
```

### Check Running Processes
```bash
# View processes in container
docker compose top backend
docker compose top frontend

# View all processes
docker compose top
```

## 📝 Environment & Configuration

### View Environment Variables
```bash
# Show all env vars in container
docker compose exec backend env
docker compose exec frontend env

# Show specific env var
docker compose exec backend bash -c 'echo $DATABASE_URL'
docker compose exec frontend sh -c 'echo $REACT_APP_API_URL'
```

### Update Environment Variables
```bash
# 1. Update .env file
# 2. Recreate containers
docker compose up -d --force-recreate

# Or restart services
docker compose restart
```

## 🎯 Production Commands

### Deploy Production
```bash
# Build and start production services
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

# View production logs
docker compose -f docker-compose.prod.yml logs -f

# Stop production
docker compose -f docker-compose.prod.yml down
```

### Health Checks
```bash
# Test backend health
curl http://localhost:8000/api/v1/health

# Test frontend health (production)
curl http://localhost/health

# View health status
docker compose ps
```

## 💡 Tips & Tricks

### Useful Aliases
Add these to your `~/.bashrc` or `~/.zshrc`:
```bash
alias dc='docker compose'
alias dcup='docker compose up -d'
alias dcdown='docker compose down'
alias dclogs='docker compose logs -f'
alias dcps='docker compose ps'
alias dcbuild='docker compose build'
alias dcrestart='docker compose restart'
```

### Quick Commands
```bash
# Restart backend after code changes (if hot-reload fails)
dc restart backend

# View last 50 lines of backend logs
dc logs --tail=50 backend

# Execute interactive python shell
dc exec backend python

# Execute interactive node shell
dc exec frontend node

# Check if database is ready
dc exec postgres pg_isready -U vibe_user

# Clear Redis cache
dc exec redis redis-cli FLUSHDB
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
