# Quick Start Guide

Get the Vibe Fitness Platform up and running in minutes!

## 🚀 Fastest Way (Docker)

```bash
# 1. Start all services (PostgreSQL, Redis, Backend, Frontend)
docker compose up -d

# 2. Run database migrations
docker compose exec backend alembic upgrade head

# 3. Seed sample data (optional)
docker compose exec backend python -m app.db.seed

# 4. Open your browser
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

**Services Available:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

**Sample Login Credentials:**
- Admin: `admin@vibe.com` / `admin123`
- Coach: `coach@vibe.com` / `coach123`
- Client: `client@vibe.com` / `client123`

---

## 📋 Prerequisites

### For Docker Setup (Recommended)
- Docker Desktop installed (includes Docker and Docker Compose)
- That's it! 🎉

**What you get with Docker:**
- ✅ PostgreSQL database (with persistent storage)
- ✅ Redis cache (for sessions and caching)
- ✅ Backend API (with hot-reload)
- ✅ Frontend app (with hot-reload)
- ✅ Automatic service networking
- ✅ Health checks for all services

### For Local Setup
- Python 3.11+
- PostgreSQL 16+
- pip

---

## 🐳 Docker Setup (Recommended)

### Start All Services
```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker compose up -d
```

### Stop Services
```bash
# Stop all services
docker compose down

# Stop and remove all data
docker compose down -v
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Access Databases
```bash
# PostgreSQL
docker compose exec postgres psql -U vibe_user -d vibe_db

# Redis
docker compose exec redis redis-cli
```

---

## 💻 Local Setup (Without Docker)

### 1. Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE USER vibe_user WITH PASSWORD 'vibe_password';
CREATE DATABASE vibe_db OWNER vibe_user;
\q
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set DATABASE_URL=postgresql+asyncpg://vibe_user:vibe_password@localhost:5432/vibe_db
```

### 3. Run Migrations
```bash
alembic upgrade head
```

### 4. Start Server
```bash
uvicorn app.main:app --reload
```

---

## 🔧 Common Commands

### Database Migrations
```bash
# With Docker
docker compose exec backend alembic upgrade head
docker compose exec backend alembic current
docker compose exec backend alembic history

# Without Docker
alembic upgrade head
./scripts/db_migrate.sh upgrade
```

### Create New Migration
```bash
# With Docker
docker compose exec backend alembic revision --autogenerate -m "description"

# Without Docker
alembic revision --autogenerate -m "description"
./scripts/db_migrate.sh autogenerate "description"
```

### Seed Database
```bash
# With Docker
docker compose exec backend python -m app.db.seed

# Without Docker
python -m app.db.seed
```

### Run Tests
```bash
# With Docker
docker compose exec backend pytest

# Without Docker
pytest
```

---

## 📚 Documentation

- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Comprehensive Docker guide
- **[backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)** - Database setup and operations
- **[backend/RUNBOOK.md](backend/RUNBOOK.md)** - Operations manual
- **[backend/README.md](backend/README.md)** - Backend documentation

---

## 🔍 Verification

### Check Services
```bash
# Docker
docker compose ps

# Should show:
# vibe_postgres  - healthy
# vibe_redis     - healthy
# vibe_backend   - healthy
# vibe_frontend  - running
```

### Test API
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Should return:
# {"status":"healthy",...}
```

### Check Database
```bash
# With Docker
docker compose exec postgres psql -U vibe_user -d vibe_db -c "\dt"

# Should show 5 tables:
# users, workout_logs, diet_logs, workout_plans, diet_plans
```

---

## 📊 What's Included

### Data Models
- **User** - User accounts (client, coach, admin roles)
- **WorkoutLog** - Workout session tracking
- **DietLog** - Meal and nutrition tracking
- **WorkoutPlan** - Structured workout programs
- **DietPlan** - Structured diet programs

### API Endpoints
- `GET /` - Welcome message
- `GET /api/v1/health` - Health check
- `GET /api/docs` - Interactive API documentation

---

## ❓ Need Help?

### Troubleshooting

**Port already in use?**
```bash
# Change ports in docker-compose.yml
# Or stop conflicting service:
lsof -i :8000
lsof -i :5432
```

**Can't connect to database?**
```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Check DATABASE_URL
cat backend/.env | grep DATABASE_URL
```

**Migration errors?**
```bash
# Check current state
alembic current

# Reset if needed
alembic stamp head
alembic upgrade head
```

### Get More Help
- Check the [RUNBOOK.md](backend/RUNBOOK.md) for detailed procedures
- See [DATABASE_SETUP.md](backend/DATABASE_SETUP.md) for database issues
- Review [DOCKER_SETUP.md](DOCKER_SETUP.md) for Docker problems

---

## 🎯 Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/api/docs
   - Try the health check endpoint
   - Review the data models

2. **Add your features**
   - Create new models in `backend/app/models/`
   - Add endpoints in `backend/app/api/v1/`
   - Generate migrations with Alembic

3. **Deploy to production**
   - Review security settings
   - Set production environment variables
   - Configure proper database
   - Set up monitoring

---

Happy coding! 🚀
