# Backend Scripts

This directory contains utility scripts for database operations and other backend tasks.

## Database Migration Script

`db_migrate.sh` - Helper script for Alembic database migrations

### Usage

```bash
# Make sure you're in the backend directory and have activated the virtual environment
cd backend
source venv/bin/activate

# Run the script
./scripts/db_migrate.sh <command> [options]
```

### Commands

#### Upgrade Database
```bash
# Upgrade to the latest version
./scripts/db_migrate.sh upgrade

# Upgrade to a specific version
./scripts/db_migrate.sh upgrade abc123
```

#### Downgrade Database
```bash
# Downgrade by one version
./scripts/db_migrate.sh downgrade

# Downgrade to a specific version
./scripts/db_migrate.sh downgrade abc123
```

#### Check Current Version
```bash
./scripts/db_migrate.sh current
```

#### View Migration History
```bash
./scripts/db_migrate.sh history
```

#### Create New Migration
```bash
# Create a blank migration file
./scripts/db_migrate.sh revision "add user phone number"

# Auto-generate migration from model changes
./scripts/db_migrate.sh autogenerate "add user preferences"
```

### Docker Usage

When using Docker, run the script inside the container:

```bash
# Upgrade database in Docker
docker-compose exec backend ./scripts/db_migrate.sh upgrade

# Auto-generate migration in Docker
docker-compose exec backend ./scripts/db_migrate.sh autogenerate "description"
```

## Tips

1. Always review auto-generated migrations before applying them
2. Test migrations on a copy of production data
3. Keep migrations small and focused
4. Write both upgrade and downgrade functions
5. Back up your database before running migrations in production
