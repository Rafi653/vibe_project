# Database Setup Guide

This guide covers PostgreSQL database setup, Alembic migrations, and database operations for the Vibe Fitness Platform.

## Table of Contents
1. [Quick Start with Docker](#quick-start-with-docker)
2. [Local PostgreSQL Setup](#local-postgresql-setup)
3. [Database Migrations with Alembic](#database-migrations-with-alembic)
4. [Seeding the Database](#seeding-the-database)
5. [Connecting to the Database](#connecting-to-the-database)
6. [Schema Changes](#schema-changes)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start with Docker

The easiest way to get started is using Docker Compose, which sets up both PostgreSQL and the backend application.

### Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

### Steps

1. **Start the services:**
   ```bash
   # From the project root directory
   docker-compose up -d
   ```

   This will:
   - Start a PostgreSQL container on port 5432
   - Start the backend application on port 8000
   - Create a persistent volume for database data

2. **Run database migrations:**
   ```bash
   # Access the backend container
   docker-compose exec backend bash
   
   # Inside the container, run migrations
   alembic upgrade head
   
   # Exit the container
   exit
   ```

3. **Seed the database (optional):**
   ```bash
   docker-compose exec backend python -m app.db.seed
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs
   - Health Check: http://localhost:8000/api/v1/health

5. **Stop the services:**
   ```bash
   docker-compose down
   
   # To also remove the database volume:
   docker-compose down -v
   ```

---

## Local PostgreSQL Setup

If you prefer to run PostgreSQL locally without Docker:

### Prerequisites
- PostgreSQL 16+ installed
- Python 3.11+ with virtual environment

### Installation

#### macOS (using Homebrew)
```bash
brew install postgresql@16
brew services start postgresql@16
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Windows
Download and install from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)

### Database Creation

1. **Create the database and user:**
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql
   
   # Or on macOS
   psql postgres
   ```

2. **Run these SQL commands:**
   ```sql
   CREATE USER vibe_user WITH PASSWORD 'vibe_password';
   CREATE DATABASE vibe_db OWNER vibe_user;
   GRANT ALL PRIVILEGES ON DATABASE vibe_db TO vibe_user;
   
   -- Exit psql
   \q
   ```

3. **Update your .env file:**
   ```bash
   cd backend
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   ```
   DATABASE_URL=postgresql+asyncpg://vibe_user:vibe_password@localhost:5432/vibe_db
   ```

4. **Install Python dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

---

## Database Migrations with Alembic

Alembic is used for database schema version control and migrations.

### Common Commands

#### Check current migration status
```bash
alembic current
```

#### View migration history
```bash
alembic history --verbose
```

#### Upgrade to latest version
```bash
alembic upgrade head
```

#### Upgrade to specific version
```bash
alembic upgrade <revision_id>
```

#### Downgrade one version
```bash
alembic downgrade -1
```

#### Downgrade to specific version
```bash
alembic downgrade <revision_id>
```

#### View SQL without executing
```bash
alembic upgrade head --sql
```

---

## Seeding the Database

The seed script populates the database with initial test data.

### Running the Seed Script

**With Docker:**
```bash
docker-compose exec backend python -m app.db.seed
```

**Local Development:**
```bash
source venv/bin/activate  # Activate virtual environment
python -m app.db.seed
```

### Sample Data Created

The seed script creates:
- **3 Users:**
  - Admin: admin@vibe.com / admin123
  - Coach: coach@vibe.com / coach123
  - Client: client@vibe.com / client123
- **1 Sample Workout Log** for the client
- **1 Sample Diet Log** for the client
- **1 Sample Workout Plan** for the client
- **1 Sample Diet Plan** for the client

---

## Connecting to the Database

### Using psql

**With Docker:**
```bash
# Connect to the PostgreSQL container
docker-compose exec postgres psql -U vibe_user -d vibe_db
```

**Local PostgreSQL:**
```bash
psql -U vibe_user -d vibe_db -h localhost
```

### Common psql Commands

```sql
-- List all tables
\dt

-- Describe a table
\d users

-- List all databases
\l

-- List all users
\du

-- Execute a query
SELECT * FROM users;

-- Quit psql
\q
```

### Using a GUI Client

Popular PostgreSQL GUI clients:
- **pgAdmin 4** - https://www.pgadmin.org/
- **DBeaver** - https://dbeaver.io/
- **DataGrip** - https://www.jetbrains.com/datagrip/
- **TablePlus** - https://tableplus.com/

**Connection Details:**
- Host: `localhost` (or `127.0.0.1`)
- Port: `5432`
- Database: `vibe_db`
- User: `vibe_user`
- Password: `vibe_password`

---

## Schema Changes

### Making Schema Changes

1. **Update your SQLAlchemy models** in `app/models/`

2. **Generate a new migration:**
   ```bash
   # This will auto-detect changes and create a migration file
   alembic revision --autogenerate -m "Description of changes"
   ```

3. **Review the generated migration** in `alembic/versions/`
   - Alembic may not detect all changes (e.g., column renames)
   - Always review and test migrations before applying

4. **Apply the migration:**
   ```bash
   alembic upgrade head
   ```

### Manual Migration Example

If you need to create a migration manually:

```bash
alembic revision -m "add_user_phone_number"
```

Edit the generated file:
```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
```

### Best Practices

1. **Always test migrations on a copy of production data first**
2. **Write both upgrade and downgrade functions**
3. **Keep migrations small and focused**
4. **Add indexes for frequently queried columns**
5. **Use transactions for data migrations**
6. **Document complex migrations**

---

## Troubleshooting

### Connection Refused Error

**Problem:** Cannot connect to PostgreSQL

**Solutions:**
```bash
# Check if PostgreSQL is running
docker-compose ps  # For Docker
sudo systemctl status postgresql  # For local PostgreSQL

# Check if the port is accessible
telnet localhost 5432

# Verify DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Migration Conflicts

**Problem:** "Can't locate revision identified by..."

**Solution:**
```bash
# Check current database version
alembic current

# Check available migrations
alembic history

# If needed, stamp the database to a specific version
alembic stamp head
```

### Database Already Exists

**Problem:** "database already exists" error

**Solution:**
```bash
# Drop and recreate the database
docker-compose down -v  # For Docker
# Or manually:
psql -U postgres -c "DROP DATABASE vibe_db;"
psql -U postgres -c "CREATE DATABASE vibe_db OWNER vibe_user;"
```

### Permission Denied

**Problem:** Permission issues with PostgreSQL

**Solution:**
```sql
-- Connect as postgres superuser
psql -U postgres

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE vibe_db TO vibe_user;
GRANT ALL ON SCHEMA public TO vibe_user;
```

### Checking Logs

**Docker:**
```bash
# Backend logs
docker-compose logs backend

# PostgreSQL logs
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f
```

**Local:**
```bash
# PostgreSQL logs location varies by OS
# Ubuntu/Debian:
sudo tail -f /var/log/postgresql/postgresql-16-main.log

# macOS (Homebrew):
tail -f /opt/homebrew/var/log/postgresql@16.log
```

---

## Data Models

### Users
- Stores user accounts (clients, coaches, admins)
- Fields: email, hashed_password, full_name, role, is_active, is_verified

### WorkoutLog
- Tracks individual workout sessions
- Fields: user_id, workout_date, exercise_name, sets, reps, weight, duration_minutes, notes

### DietLog
- Tracks daily meals and nutrition
- Fields: user_id, meal_date, meal_type, food_name, calories, protein/carbs/fat, notes

### WorkoutPlan
- Defines structured workout programs
- Fields: user_id, name, description, start/end dates, status, duration_weeks, workout_details (JSON)

### DietPlan
- Defines structured diet programs
- Fields: user_id, name, description, start/end dates, status, nutritional targets, meal_plan_details (JSON)

---

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
