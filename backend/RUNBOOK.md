# Vibe Fitness Platform - Operational Runbook

This runbook provides step-by-step procedures for common operational tasks.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Daily Operations](#daily-operations)
3. [Database Operations](#database-operations)
4. [Deployment](#deployment)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)

---

## Initial Setup

### First-Time Setup with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rafi653/vibe_project.git
   cd vibe_project
   ```

2. **Start the services**
   ```bash
   docker compose up -d
   ```
   
   This starts:
   - PostgreSQL database (port 5432)
   - Backend API (port 8000)

3. **Run database migrations**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

4. **Seed the database (optional, for development)**
   ```bash
   docker compose exec backend python -m app.db.seed
   ```

5. **Verify the setup**
   - Health check: http://localhost:8000/api/v1/health
   - API docs: http://localhost:8000/api/docs

### First-Time Setup Without Docker

1. **Prerequisites**
   - Install PostgreSQL 16+
   - Install Python 3.11+

2. **Set up PostgreSQL**
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql
   
   # Create database and user
   CREATE USER vibe_user WITH PASSWORD 'vibe_password';
   CREATE DATABASE vibe_db OWNER vibe_user;
   GRANT ALL PRIVILEGES ON DATABASE vibe_db TO vibe_user;
   \q
   ```

3. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set DATABASE_URL for local PostgreSQL:
   # DATABASE_URL=postgresql+asyncpg://vibe_user:vibe_password@localhost:5432/vibe_db
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Daily Operations

### Starting the Application

**With Docker:**
```bash
docker compose up -d
```

**Without Docker:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Stopping the Application

**With Docker:**
```bash
# Stop services
docker compose down

# Stop and remove data volumes
docker compose down -v
```

**Without Docker:**
```bash
# Press Ctrl+C in the terminal running uvicorn
```

### Viewing Logs

**With Docker:**
```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# PostgreSQL only
docker compose logs -f postgres
```

**Without Docker:**
- Logs appear in the terminal where uvicorn is running
- Check application logs in `logs/` directory if configured

### Health Checks

```bash
# Check API health
curl http://localhost:8000/api/v1/health

# Check if services are running (Docker)
docker compose ps
```

---

## Database Operations

### Running Migrations

**With Docker:**
```bash
# Upgrade to latest
docker compose exec backend alembic upgrade head

# Check current version
docker compose exec backend alembic current

# View history
docker compose exec backend alembic history
```

**Without Docker:**
```bash
cd backend
source venv/bin/activate

# Upgrade to latest
alembic upgrade head

# Or use the helper script
./scripts/db_migrate.sh upgrade
```

### Creating New Migrations

**When you modify models:**

1. **Auto-generate migration**
   ```bash
   # With Docker
   docker compose exec backend alembic revision --autogenerate -m "description of changes"
   
   # Without Docker
   cd backend
   alembic revision --autogenerate -m "description of changes"
   # Or use the helper script
   ./scripts/db_migrate.sh autogenerate "description of changes"
   ```

2. **Review the generated migration**
   ```bash
   # Check the new file in backend/alembic/versions/
   ls -lt backend/alembic/versions/
   ```

3. **Apply the migration**
   ```bash
   # With Docker
   docker compose exec backend alembic upgrade head
   
   # Without Docker
   alembic upgrade head
   ```

### Rolling Back Migrations

```bash
# Rollback one version
docker compose exec backend alembic downgrade -1

# Rollback to specific version
docker compose exec backend alembic downgrade <revision_id>
```

### Connecting to the Database

**With Docker:**
```bash
docker compose exec postgres psql -U vibe_user -d vibe_db
```

**Without Docker:**
```bash
psql -U vibe_user -d vibe_db -h localhost
```

**Common SQL queries:**
```sql
-- List all tables
\dt

-- Count users
SELECT COUNT(*) FROM users;

-- View recent workout logs
SELECT * FROM workout_logs ORDER BY created_at DESC LIMIT 10;

-- Check table structure
\d users
```

### Database Backup

**With Docker:**
```bash
# Backup
docker compose exec postgres pg_dump -U vibe_user vibe_db > backup_$(date +%Y%m%d).sql

# Restore
docker compose exec -T postgres psql -U vibe_user -d vibe_db < backup_20251011.sql
```

**Without Docker:**
```bash
# Backup
pg_dump -U vibe_user -d vibe_db -h localhost > backup_$(date +%Y%m%d).sql

# Restore
psql -U vibe_user -d vibe_db -h localhost < backup_20251011.sql
```

### Seeding the Database

```bash
# With Docker
docker compose exec backend python -m app.db.seed

# Without Docker
cd backend
source venv/bin/activate
python -m app.db.seed
```

---

## Deployment

### Production Deployment Checklist

- [ ] Update environment variables in `.env`
  - [ ] Set strong SECRET_KEY
  - [ ] Set ENVIRONMENT=production
  - [ ] Set DEBUG=false
  - [ ] Configure production DATABASE_URL
  
- [ ] Run database migrations
  ```bash
  alembic upgrade head
  ```

- [ ] Test all endpoints
  ```bash
  # Run test suite
  pytest
  ```

- [ ] Verify database connectivity
  ```bash
  # Test connection
  python -c "from app.db.base import engine; import asyncio; asyncio.run(engine.connect())"
  ```

- [ ] Check application logs
- [ ] Set up monitoring and alerting
- [ ] Configure backup schedules

### Building for Production

**Update Dockerfile for production:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

## Troubleshooting

### Common Issues

#### Cannot Connect to Database

**Symptoms:** Connection refused or timeout errors

**Solutions:**
1. Check if PostgreSQL is running:
   ```bash
   # Docker
   docker compose ps postgres
   
   # Local
   sudo systemctl status postgresql
   ```

2. Verify DATABASE_URL in `.env`
   ```bash
   cat backend/.env | grep DATABASE_URL
   ```

3. Test connection:
   ```bash
   # Docker
   docker compose exec backend python -c "from app.db.base import engine; print('OK')"
   ```

#### Migration Conflicts

**Symptoms:** "Can't locate revision" errors

**Solutions:**
1. Check current state:
   ```bash
   alembic current
   alembic history
   ```

2. Stamp database to correct version:
   ```bash
   alembic stamp head
   ```

3. Try migration again:
   ```bash
   alembic upgrade head
   ```

#### Port Already in Use

**Symptoms:** "Address already in use" error

**Solutions:**
1. Check what's using the port:
   ```bash
   lsof -i :8000  # Backend
   lsof -i :5432  # PostgreSQL
   ```

2. Stop the conflicting service or change ports in `docker-compose.yml`

#### Container Won't Start

**Symptoms:** Container exits immediately

**Solutions:**
1. Check logs:
   ```bash
   docker compose logs backend
   docker compose logs postgres
   ```

2. Rebuild containers:
   ```bash
   docker compose down -v
   docker compose build --no-cache
   docker compose up -d
   ```

---

## Maintenance

### Regular Tasks

#### Daily
- [ ] Check application logs for errors
- [ ] Monitor API health endpoint
- [ ] Review database connection pool

#### Weekly
- [ ] Review and archive old logs
- [ ] Check disk space usage
- [ ] Update dependencies if needed
- [ ] Review database query performance

#### Monthly
- [ ] Database backup verification
- [ ] Security updates
- [ ] Performance metrics review
- [ ] Database optimization (VACUUM, ANALYZE)

### Database Maintenance

**Optimize database:**
```sql
-- Connect to database
psql -U vibe_user -d vibe_db

-- Analyze tables
ANALYZE users;
ANALYZE workout_logs;
ANALYZE diet_logs;
ANALYZE workout_plans;
ANALYZE diet_plans;

-- Vacuum
VACUUM ANALYZE;

-- Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Updating Dependencies

```bash
# Update Python packages
cd backend
source venv/bin/activate
pip list --outdated
pip install --upgrade <package-name>
pip freeze > requirements.txt

# Test after updates
pytest
```

### Log Rotation

**Docker logs:**
```bash
# View log size
docker compose logs backend --no-color | wc -l

# Clear logs (will lose history)
docker compose down
docker compose up -d
```

**Application logs:**
```bash
# Configure logrotate for application logs
# Create /etc/logrotate.d/vibe-backend
```

---

## Support Contacts

- **Development Team**: [dev@vibe.com](mailto:dev@vibe.com)
- **Database Admin**: [dba@vibe.com](mailto:dba@vibe.com)
- **DevOps**: [devops@vibe.com](mailto:devops@vibe.com)

---

## Related Documentation

- [README.md](README.md) - General project information
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Detailed database setup guide
- [DOCKER_SETUP.md](../DOCKER_SETUP.md) - Docker-specific documentation
- [API Documentation](http://localhost:8000/api/docs) - Interactive API docs
