# Docker Quick Reference

Quick commands for common Docker operations with the Vibe Project.

## Development

### Start Everything
```bash
docker compose up -d
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
```

### Stop Everything
```bash
docker compose down
```

### Restart a Service
```bash
docker compose restart backend
docker compose restart frontend
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker compose up -d --build

# Rebuild specific service
docker compose build backend
docker compose up -d backend
```

## Database Operations

### Run Migrations
```bash
docker compose exec backend alembic upgrade head
```

### Create New Migration
```bash
docker compose exec backend alembic revision --autogenerate -m "description"
```

### Seed Database
```bash
docker compose exec backend python -m app.db.seed
```

### Connect to Database
```bash
docker compose exec postgres psql -U vibe_user -d vibe_db
```

### Backup Database
```bash
docker compose exec postgres pg_dump -U vibe_user vibe_db > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker compose exec -T postgres psql -U vibe_user -d vibe_db
```

## Testing

### Backend Tests
```bash
docker compose exec backend pytest
docker compose exec backend pytest -v
docker compose exec backend pytest tests/test_health.py
```

### Frontend Tests
```bash
docker compose exec frontend npm test
```

## Shell Access

### Backend Shell
```bash
docker compose exec backend bash
```

### Frontend Shell
```bash
docker compose exec frontend sh
```

### Database Shell
```bash
docker compose exec postgres psql -U vibe_user -d vibe_db
```

## Troubleshooting

### Check Service Status
```bash
docker compose ps
```

### Check Service Health
```bash
docker compose ps
docker inspect vibe_backend | grep Health -A 10
```

### View Container Resource Usage
```bash
docker stats
```

### Clean Up
```bash
# Remove stopped containers
docker compose down

# Remove volumes (deletes all data!)
docker compose down -v

# Clean up Docker system
docker system prune
```

## Production

### Deploy Production
```bash
# Set environment variables
cp .env.example .env
# Edit .env with production values

# Start production services
docker compose -f docker-compose.prod.yml up -d

# Run migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Production Logs
```bash
docker compose -f docker-compose.prod.yml logs -f
```

### Production Stop
```bash
docker compose -f docker-compose.prod.yml down
```

## Access URLs

### Development
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/v1/health

### Production
- Frontend: http://localhost (port 80)
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/v1/health

## Helpful Tips

1. **Hot Reload**: Both frontend and backend support hot reload in development mode
2. **Data Persistence**: Database data persists in Docker volumes even after `docker compose down`
3. **Clean Restart**: Use `docker compose down -v` to start fresh (deletes all data)
4. **Network Issues**: If containers can't communicate, check `docker network ls` and `docker compose ps`
5. **Port Conflicts**: If ports are in use, change them in docker-compose.yml or stop conflicting services

## Common Issues

### Container Won't Start
```bash
docker compose logs <service-name>
docker compose down -v
docker compose up -d
```

### Can't Connect to Backend from Frontend
```bash
# Check if backend is running
curl http://localhost:8000/api/v1/health
# Check CORS settings in backend
```

### Database Connection Failed
```bash
# Check if database is healthy
docker compose ps
# Check database logs
docker compose logs postgres
```

For more details, see [DOCKER_SETUP.md](DOCKER_SETUP.md).
